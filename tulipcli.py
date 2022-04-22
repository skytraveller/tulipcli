#!/usr/bin/env python3

import author
import argparse
import database
import os
import platform
import sys


def TulipcliParser():
    args = argparse.ArgumentParser()
    args.add_argument("-db", "--database", default=":memory:", type=str)
    args.add_argument("-nv", "--noversion", action="store_true")

    args.add_argument("-ds", "--description", default="", type=str)
    args.add_argument("-na", "--name", default="", type=str)
    args.add_argument("-pa", "--parent", default=0, type=int)
    args.add_argument("-ui", "--uid", default=0, type=int)

    args.add_argument("-de", "--delete", action="store_true")
    args.add_argument("-fi", "--find", default="", type=str)
    args.add_argument("-fs", "--findsplit", default=",", type=str)
    args.add_argument("-re", "--read", default=[], nargs="+", type=str)
    args.add_argument("-se", "--search", action="store_true")
    args.add_argument("-up", "--update", action="store_true")
    args.add_argument("-write", "--write", action="store_true")
    return args


def Tulipcli(**kwargs):
    if db := kwargs.get("database", ":memory:"):
        with database.SqlDatabase().open(db) as db:

            cliitem = {}
            for a in ("description", "name", "parent", "uid"):
                b = kwargs.get(a)
                if b is not None:
                    cliitem.update({a: b})

            if kwargs.get("delete"):
                if "uid" in cliitem:
                    if item := db.getitemsquery(uid=cliitem["uid"]).first():
                        item.delete(db)
                        return " ".join(("Deleted", str(cliitem["uid"])))
                    else:
                        return " ".join((
                            "Item",
                            str(cliitem["uid"]),
                            "not found"
                        ))

            if kfind := kwargs.get("find"):
                if isinstance(kfind, str):
                    kfind = kfind.split(kwargs.get("findsplit", ","))
                if r := db.find(*kfind):
                    r = r.__str__(database=db)
                return r

            if kread := kwargs.get("read"):
                if isinstance(kread, list):
                    kread = " ".join(kread)
                if isinstance(kread, str):
                    if os.path.isfile(kread):
                        with open(kread, "r") as f:
                            kread = f.read()
                if isinstance(kread, str):
                    try:
                        kread = eval(kread)
                    except SyntaxError as se:
                        return "Unable to read data. " + str(se)
                db.read(kread)
                return "Item(s) imported"

            if kwargs.get("search"):
                return [a.__str__(database=db) for a in db.search(
                    description=kwargs.get("description"),
                    name=kwargs.get("name"),
                )]

            if kwargs.get("update"):
                if "uid" in cliitem:
                    if item := db.getitemsquery(uid=cliitem["uid"]).first():
                        [setattr(item, k, kwargs[k]) for k in cliitem]
                        cliitem = item
                    else:
                        cliitem = database.Item(**cliitem)
                        db.session.add(cliitem)
                db.session.commit()
                return str(cliitem)

            if kwargs.get("write") and "uid" in cliitem:
                if item := db.getitemsquery(uid=cliitem["uid"]).first():
                    return item.__str__(database=db)
                else:
                    return " ".join(("Item", str(cliitem["uid"]), "not found"))

    return None


if __name__ == "__main__":
    args = TulipcliParser().parse_args()
    if not args.noversion:
        print(" ".join([
            author.__title__,
            author.__version__,
            platform.system(),
            platform.architecture()[0],
            platform.python_implementation(),
            ".".join((str(a) for a in sys.version_info)),
        ]))
    if r := Tulipcli(**vars(args)):
        print(r)
