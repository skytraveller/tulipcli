
import collections.abc
import sqlalchemy
import sqlalchemy.ext.declarative

db = sqlalchemy.ext.declarative.declarative_base()


class Item(db):
    __tablename__ = "items"
    description = sqlalchemy.Column(sqlalchemy.String(), default="")
    name = sqlalchemy.Column(sqlalchemy.String(), default="")
    parent = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    uid = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)

    def __str__(self, depth=1000, database=None, **kwargs):
        return str(self.asdict(depth, database, **kwargs))

    def asdict(self, depth=1000, database=None, **kwargs):
        ret = {
            self.name: {},
        }
        for a in [
            "description",
            "parent",
            "uid",
        ]:
            if kwargs.get(a, True):
                b = getattr(self, a)
                if b is not None:
                    ret = updatenested(ret, {self.name: {a: b}})
        if database and depth:
            depth -= 1
            for a in database.getitemsquery(parent=self.uid, **kwargs).all():
                ret[self.name] = updatenested(
                    ret[self.name],
                    a.asdict(depth, **kwargs)
                )
        return ret

    def delete(self, db, commit=True):
        [a.delete(db, False) for a in db.getitemsquery(parent=self.uid).all()]
        db.session.delete(self)
        if commit:
            db.session.commit()
        return self


class SqlDatabase:
    __slots__ = (
        "engine",
        "path",
        "session",
    )

    def __enter__(self):
        return self

    def __init__(self, **kwargs):
        self.engine = None
        self.path = ""
        self.session = None
        [setattr(self, k, kwargs[k]) for k in kwargs]

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        self.session.close()
        return self

    def find(self, *names, parent=0):
        r = self.session.query(Item).filter_by(
            name=names[0]
        ).filter_by(
            parent=parent
        ).first()
        for a in names[1:]:
            if r:
                if b := self.session.query(Item).filter_by(
                    name=a
                ).filter_by(
                    parent=r.uid
                ).first():
                    r = b
        return r

    def getitemsquery(self, **kwargs):
        r = self.session.query(Item)
        if name := kwargs.get("name", None):
            r = r.filter_by(name=name)
        parent = kwargs.get("parent", None)
        if parent is not None:
            r = r.filter_by(parent=parent)
        if uid := kwargs.get("uid", None):
            r = r.filter_by(uid=uid)
        for a in kwargs.get("orderby", []):
            r = r.order_by(a)
        if offset := kwargs.get("offset", 0):
            r = r.offset(offset)
        if limit := kwargs.get("limit", 0):
            r = r.limit(limit)
        return r

    def open(self, path=None, echo=False):
        if not path:
            path = self.path
        self.path = path
        self.engine = sqlalchemy.create_engine(
            "sqlite:///" + path,
            echo=echo
        )
        db.metadata.create_all(self.engine)
        self.session = sqlalchemy.orm.sessionmaker(bind=self.engine)()
        return self

    def read(self, src, parent=0):
        props = [
            "uid",
            "description",
            "parent",
            "owner",
        ]

        def recurcreate(d, parentidd=0):

            def x(namee, xpid, children=[]):
                if i := self.session.query(Item).filter_by(
                    name=namee
                ).filter_by(
                    parent=xpid
                ).first():
                    pass
                else:
                    i = Item(name=namee, parent=xpid)
                [setattr(i, a, children[a]) for a in props if a in children]
                self.session.add(i)
                self.session.commit()
                return i

            def xdict(namee, parentidddd, children, pid=None):
                if pid is None:
                    pid = x(namee, parentidddd, children)
                for a in children:
                    if a not in props:
                        if isinstance(children[a], dict):
                            xdict(a, pid.uid, children[a])
                        else:
                            recurcreate(children[a], pid.uid)
                self.session.commit()
                return pid.uid

            if isinstance(d, int):
                d = str(d)
            if isinstance(d, str):
                x(d, parentidd)
            elif isinstance(d, list) or isinstance(d, tuple):
                [recurcreate(a, parentidd) for a in d]
            elif isinstance(d, dict):
                [xdict(a, parentidd, d[a]) for a in d]

        recurcreate(src, parent)
        self.session.commit()
        return "Items imported"

    def search(self, name=None, description=None, **kwargs):
        r = self.session.query(Item)
        if description and name:
            df = Item.description.like("%" + description + "%")
            nf = Item.name.like("%" + name + "%")
            if not description or not name:
                if description:
                    r = r.filter(df)
                if name:
                    r = r.filter(nf)
            else:
                r = r.filter(sqlalchemy.or_(df, nf))
        parent = kwargs.get("parent", None)
        if parent is not None:
            r = r.filter_by(parent=parent)
        if uid := kwargs.get("uid", None):
            r = r.filter_by(uid=uid)
        return r.all()


def updatenested(self, values, ignore=[]):
    self = dict(self)
    for k, v in values.items():
        if k not in ignore:
            if isinstance(v, collections.abc.Mapping):
                self[k] = updatenested(self.get(k, {}), v)
            else:
                self[k] = v
    return self
