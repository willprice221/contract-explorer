from copy import copy

test = ['if','sth',['add',2,3]]
example = [["IF", ["ISZERO", ["EQ", ["STORAGE", 160, 0, 0], "CALLER"]], [["REVERT", 0]], [["IF", ["ISZERO", ["EXTCODESIZE", ["MASK_SHL", 160, 0, 0, ["cd", 4]]]], [["REVERT", 0]], [["CALL", ["ADD", -710, "GAS"], ["MASK_SHL", 160, 0, 0, ["cd", 4]], 0, 1981353871, 'null'], ["IF", ["ISZERO", "ext_call.success"], [["REVERT", 0]], [["IF", ["ISZERO", "ext_call.return_data"], [["REVERT", 0]], [["STORE", 160, 0, 12, [], ["MASK_SHL", 160, 0, 0, ["cd", 4]]], ["STOP"]]]]]]]]]]
example2 = [["IF", ["ISZERO", ["STORAGE", 160, 0, 0]], [["STORE", 256, 0, 2, [["MASK_SHL", 256, 0, 0, ["SHA3", "CALLER", 7]], ["MASK_SHL", 160, 0, 0, ["cd", 4]]], ["cd", 36]], ["LOG", ["MASK_SHL", 256, 0, 0, ["cd", 36]], 63486140976153616755203102783360879283472101686154884697241723088393386309925, "CALLER", ["MASK_SHL", 160, 0, 0, ["cd", 4]]], ["RETURN", 1]], [["IF", ["LE", ["EXTCODESIZE", ["STORAGE", 160, 0, 0]], 0], [["STORE", 256, 0, 2, [["MASK_SHL", 256, 0, 0, ["SHA3", "CALLER", 7]], ["MASK_SHL", 160, 0, 0, ["cd", 4]]], ["cd", 36]], ["LOG", ["MASK_SHL", 256, 0, 0, ["cd", 36]], 63486140976153616755203102783360879283472101686154884697241723088393386309925, "CALLER", ["MASK_SHL", 160, 0, 0, ["cd", 4]]], ["RETURN", 1]], [["IF", ["ISZERO", ["EXTCODESIZE", ["STORAGE", 160, 0, 0]]], [["REVERT", 0]], [["CALL", ["ADD", -710, "GAS"], ["STORAGE", 160, 0, 0], 0, 3664259819, ["DATA", "CALLER", ["MASK_SHL", 160, 0, 0, ["cd", 4]], ["MASK_SHL", 256, 0, 0, ["cd", 36]]]], ["IF", ["ISZERO", "ext_call.success"], [["REVERT", 0]], [["IF", ["ISZERO", "ext_call.return_data"], [["REVERT", 0]], [["STORE", 256, 0, 2, [["MASK_SHL", 256, 0, 0, ["SHA3", "CALLER", 7]], ["MASK_SHL", 160, 0, 0, ["cd", 4]]], ["cd", 36]], ["LOG", ["MASK_SHL", 256, 0, 0, ["cd", 36]], 63486140976153616755203102783360879283472101686154884697241723088393386309925, "CALLER", ["MASK_SHL", 160, 0, 0, ["cd", 4]]], ["RETURN", 1]]]]]]]]]]]]
terminal = []

class Node:

    def __repr__(self):
        if len(self.children) == 0:
            return self.name
        else:
            return f'( {self.name} '+ (' '.join([str(c) for c in self.children]))+' )'

    def __init__(self, exp, parent=None):
        self.parent = parent
        self.children = []

        if type(exp) == list and len(exp)>0:
            self.name = exp[0] if type(exp[0]) == str else 'list'
            if self.name != 'list':
                for e in exp[1:]:
                    self.children.append(Node(e, parent=self))
            else:
                for e in exp:
                    self.children.append(Node(e, parent=self))

        else:
            self.name=str(exp)
            global terminal
            terminal.append(self)

    def paths(self):
        result = []

        def dfs(node, path_so_far, ignore):
            # print(node)

            path_so_far = copy(path_so_far)
            path_so_far.append(node.name)


            if len(node.children) == 0:
                result = [path_so_far]
            else:
                result = []


            for c in node.children:
                if c is not ignore:
                    result.extend(dfs(c, path_so_far, node))

            if node.parent is not None and node.parent is not ignore:
                result.extend(dfs(node.parent, path_so_far, node))

            return result

        psf = []
        return dfs(self, psf, None)


root = Node(example2)



# print('all the paths')
count_paths = 0
for t in terminal:
    # print(t.paths())
    count_paths += len(t.paths())


print('terminal nodes:')
print(terminal)
print('\n')
print('terminal nodes count:')
print(len(terminal))
# print()
# print('path count:', count_paths)
