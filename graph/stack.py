"""
A stack is a data structure whose primary purpose is to store and
return elements in Last In First Out order. 

1. Implement the Stack class using an array as the underlying storage structure.
   Make sure the Stack tests pass.
2. Re-implement the Stack class, this time using the linked list implementation
   as the underlying storage structure.
   Make sure the Stack tests pass.
3. What is the difference between using an array vs. a linked list when 
   implementing a Stack?
"""

from linked_list import Node, LinkedList

# node0 = Node('super', Node('kala'))
# print(node0.value, node0.get_next().value)

# class Stack:
#     '''
#     Stack() class based in arrays...
#     '''
#     def __init__(self):
#         self.storage = []
#         self.size = 0

#     def __len__(self):
#         return len(self.storage)

#     def push(self, value):
#         self.storage.append(value)

#     def pop(self):
#         if self.storage == []:
#             self.popr = None
#         else:
#             self.popr = self.storage[-1]
#             self.storage.pop()
#         return self.popr


class Stack:
    '''
    Stack() class built on Linked Lists
    '''
    def __init__(self):
        self.size = 0
        self.storage = LinkedList()

    def __len__(self):
        return self.storage.length
        
    def push(self, value):
        self.storage.add_to_tail(value)

    def pop(self):
        return self.storage.remove_tail()