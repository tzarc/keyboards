#!/usr/bin/env python
import sys, pprint, copy
from string import whitespace
import re

dbg = False

term_regex = r'''(?mx)
    \s*(?:
        (?P<brackl>\()|
        (?P<brackr>\))|
#        (?P<num>\-?\d+\.\d+|\-?\d+)|
        (?P<sq>"[^"]*")|
        (?P<s>[^(^)\s]+)
       )'''

def parse_sexp(sexp):
    stack = []
    out = []
    if dbg: print("%-6s %-14s %-44s %-s" % tuple("term value out stack".split()))
    for termtypes in re.finditer(term_regex, sexp):
        term, value = [(t,v) for t,v in termtypes.groupdict().items() if v][0]
        if dbg: print("%-7s %-14s %-44r %-r" % (term, value, out, stack))
        if term == 'brackl':
            stack.append(out)
            out = []
        elif term == 'brackr':
            assert stack, "Trouble with nesting of brackets"
            tmpout, out = out, stack.pop(-1)
            out.append(tmpout)
        elif term == 'num':
            v = float(value)
            if v.is_integer(): v = int(v)
            out.append(v)
        elif term == 'sq':
            out.append(value[1:-1])
        elif term == 's':
            out.append(value)
        else:
            raise NotImplementedError("Error: %r" % (term, value))
    assert not stack, "Trouble with nesting of brackets"
    return out[0]

def print_sexp(exp):
    out = ''
    if type(exp) == type([]):
        out += '(' + ' '.join(print_sexp(x) for x in exp) + ')'
    elif type(exp) == type('') and re.search(r'[\s()]', exp):
        out += '"%s"' % repr(exp)[1:-1].replace('"', '\"')
    else:
        out += '%s' % exp
    return out

def get_entry(obj, name):
    for item in obj:
        if type(item) is list and len(item) > 0 and item[0] == name:
            return item
    return None

def handle_passthru(cfg, obj, args):
    return obj

def handle_fp_convertlayer(cfg, obj, args):
    layer = get_entry(obj, "layer")
    if layer[1] in args:
        layer[1] = args[layer[1]]
    else:
        return None
    return obj

def handle_fp_text(cfg, obj, args):
    if obj[1] == "value" and obj[2] == "Djinn_Layout_Full":
        obj[2] = args["name"]
        return obj
    if obj[1] == "reference":
        return obj
    return handle_fp_convertlayer(cfg, obj, args)

def handle_pad(cfg, obj, args):
    pad_char = args
    layers = obj[1]
    obj[1] = "~" if "1" not in obj[1] else "1"
    if pad_char not in layers:
        return None
    return obj

def build_output(orig, name, cfg):
    output = []
    output.append("module")
    output.append(name)

    # First two items are "module" and "footprint name", we can safely ignore them
    orig.pop(0)
    orig.pop(0)

    # Start parsing...
    for item in orig:
        if type(item) is list:
            if item[0] in cfg:
                entry = cfg[item[0]]
                args = entry["args"] if "args" in entry else None
                result = entry["handler"](cfg, copy.deepcopy(item), args)
                if result != None:
                    output.append(result)

    return output

def generate_one(name, pad_char, convert_args):
    with open("DjinnFootprints/Djinn_Layout_Full.kicad_mod", "r") as f:
        content = "\n".join([x.strip() for x in f.readlines()])
        sexpr = parse_sexp(content)

        convert_args["name"] = name
        output_args = {"handler": handle_fp_convertlayer, "args":convert_args}
        result = build_output(sexpr, name, {
            "tedit": {"handler": handle_passthru},
            "layer": {"handler": handle_passthru},
            "pad": {"handler": handle_pad, "args":pad_char},
            "fp_text": {"handler": handle_fp_text, "args":convert_args},
            "fp_line": output_args,
            "fp_circle": output_args,
            "fp_arc": output_args
        })

        with open("DjinnFootprints/%s.kicad_mod" % (name), "w") as outfile:
            outfile.write(print_sexp(result))

generate_one("Djinn_PlatePCB", 'P',{
    "Cmts.User": "Edge.Cuts",
    "B.Paste": "Edge.Cuts",
    "Eco1.User": "Edge.Cuts",
    "Eco2.User": "Dwgs.User",
    "B.SilkS": "Edge.Cuts",
    "F.CrtYd": "Dwgs.User"
})

generate_one("Djinn_MainPCB", 'M',{
    "Cmts.User": "Edge.Cuts",
    "B.Paste": "Edge.Cuts",
    "F.SilkS": "Edge.Cuts",
    "B.SilkS": "Eco1.User",
    "Eco1.User": "Dwgs.User",
    "F.CrtYd": "Dwgs.User",
    "Dwgs.User": "Dwgs.User"
})

generate_one("Djinn_BasePCB", 'B',{
    "Cmts.User": "Edge.Cuts",
    "B.Paste": "Edge.Cuts",
    "F.CrtYd": "Dwgs.User",
    "F.SilkS": "Edge.Cuts"
})

generate_one("Djinn_OutlineBottom", 'Y',{
    "Cmts.User": "Edge.Cuts",
    "B.Paste": "Edge.Cuts",
    "F.CrtYd": "Dwgs.User",
    "F.SilkS": "Edge.Cuts"
})
