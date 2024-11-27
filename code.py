class BPlusTreeNode:
    def __init__(self, leaf=False):
        self.is_leaf = leaf
        self.keys = []
        self.children = []
        self.next = None

class BPlusTree:
    def __init__(self, order):
        self.root = BPlusTreeNode(True)
        self.order = order

    def insert(self, key):
        leaf = self.find_leaf_node(key)
        index = 0
        while index < len(leaf.keys) and leaf.keys[index] < key:
            index += 1
        leaf.keys.insert(index, key)

        if len(leaf.keys) == self.order:
            new_leaf = BPlusTreeNode(True)
            mid = (self.order + 1) // 2
            new_leaf.keys = leaf.keys[mid:]
            leaf.keys = leaf.keys[:mid]

            new_leaf.next = leaf.next
            leaf.next = new_leaf

            if leaf == self.root:
                self.root = BPlusTreeNode(False)
                self.root.keys.append(new_leaf.keys[0])
                self.root.children.extend([leaf, new_leaf])
            else:
                self.insert_internal(new_leaf.keys[0], leaf, new_leaf)

    def find_leaf_node(self, key):
        cursor = self.root
        while not cursor.is_leaf:
            index = 0
            while index < len(cursor.keys) and key >= cursor.keys[index]:
                index += 1
            cursor = cursor.children[index]
        return cursor

    def insert_internal(self, key, cursor, child):
        if len(cursor.keys) < self.order - 1:
            index = 0
            while index < len(cursor.keys) and cursor.keys[index] < key:
                index += 1
            cursor.keys.insert(index, key)
            cursor.children.insert(index + 1, child)
        else:
            new_internal = BPlusTreeNode(False)
            temp_keys = cursor.keys[:]
            temp_children = cursor.children[:]

            index = 0
            while index < len(temp_keys) and temp_keys[index] < key:
                index += 1
            temp_keys.insert(index, key)
            temp_children.insert(index + 1, child)

            mid = (self.order + 1) // 2
            cursor.keys = temp_keys[:mid - 1]
            cursor.children = temp_children[:mid]

            new_internal.keys = temp_keys[mid:]
            new_internal.children = temp_children[mid:]

            if cursor == self.root:
                new_root = BPlusTreeNode(False)
                new_root.keys.append(temp_keys[mid - 1])
                new_root.children.extend([cursor, new_internal])
                self.root = new_root
            else:
                self.insert_internal(temp_keys[mid - 1], self.find_leaf_node(cursor.keys[0]), new_internal)

    def find(self, key):
        cursor = self.root
        while not cursor.is_leaf:
            index = 0
            while index < len(cursor.keys) and key >= cursor.keys[index]:
                index += 1
            cursor = cursor.children[index]
        return key in cursor.keys

    def print_tree(self, cursor=None, level=0):
        if cursor is None:
            cursor = self.root
        if cursor:
            print(f"Level {level} [ {' '.join(map(str, cursor.keys))} ]")
        if not cursor.is_leaf:
            for child in cursor.children:
                self.print_tree(child, level + 1)


class Case:
    def __init__(self, plaintiff, defendant, case_number):
        self.plaintiff = plaintiff
        self.defendant = defendant
        self.case_number = case_number

def read_and_parse_file(filename):
    cases = []
    with open(filename) as file:
        for line in file:
            match = re.match(r'(.*) v\. (.*)\((\d{5})\)', line)
            if match:
                plaintiff, defendant, case_number = match.groups()
                cases.append(Case(plaintiff, defendant, int(case_number)))
    return cases

def search_by_case_number(cases, case_number):
    return [c for c in cases if c.case_number == case_number]

def search_by_plaintiff(cases, plaintiff):
    return [c for c in cases if c.plaintiff.lower() == plaintiff.lower()]

def search_by_defendant(cases, defendant):
    return [c for c in cases if c.defendant.lower() == defendant.lower()]

def print_cases(cases):
    for c in cases:
        print(f"{c.plaintiff} v. {c.defendant} ({c.case_number})")

if __name__ == "__main__":
    import re

    filename = "court-cases.txt"
    cases = read_and_parse_file(filename)

    bpt = BPlusTree(4)
    for case_info in cases:
        bpt.insert(case_info.case_number)

    print("\nB+ Tree structure:")
    bpt.print_tree()

    search_case_number = int(input("Enter case number to search: "))
    if bpt.find(search_case_number):
        print("Case found:")
        result = search_by_case_number(cases, search_case_number)
        print_cases(result)
    else:
        print("Case not found.")

    search_choice = int(input("Search by: 1. Plaintiff 2. Defendant: "))
    search_name = input("Enter name to search: ")
    if search_choice == 1:
        result = search_by_plaintiff(cases, search_name)
        if result:
            print("Cases found:")
            print_cases(result)
        else:
            print(f"No cases found for plaintiff: {search_name}")
    elif search_choice == 2:
        result = search_by_defendant(cases, search_name)
        if result:
            print("Cases found:")
            print_cases(result)
        else:
            print(f"No cases found for defendant: {search_name}")
    else:
        print("Invalid choice.")
