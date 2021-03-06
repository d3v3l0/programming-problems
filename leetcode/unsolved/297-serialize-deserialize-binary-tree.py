"""
Serialization is the process of converting a data structure or object into a
sequence of bits so that it can be stored in a file or memory buffer, or
transmitted across a network connection link to be reconstructed later in
the same or another computer environment.

Design an algorithm to serialize and deserialize a binary tree. There
is no restriction on how your serialization/deserialization algorithm
should work. You just need to ensure that a binary tree can be serialized
to a string and this string can be deserialized to the original tree structure.

Example:
You may serialize the following tree:

    1
   / \
  2   3
     / \
    4   5

as "[1,2,3,null,null,4,5]"

Clarification: The above format is the same as how LeetCode serializes a binary tree.
You do not necessarily need to follow this format, so please be creative and come up
with different approaches yourself.

Note: Do not use class member/global/static variables to store states. Your serialize
and deserialize algorithms should be stateless.
-------------------------------------------
We will be writing two functions:

Serialize():
  input: TreeNode
  output: array

Deserialize():
  input: array
  output: TreeNode


- A serialized binary tree has the root at arr[0]. Each node at index n can
have a left or right child, which can be found at 2n+1 and 2n+2.
- Armed with this information, we can write the serialization function:
  - Start with an arbitarily sized array, say of 100 Nones
  - Recurse through the tree, starting at the node with index 0.
  - Save the left and right at 2*idx+1 and 2*idx+2.
  - If we run out of space, set array to arr + [None * len(arr)].
  - Once the recursion is complete, the tree is serialized. Vacuum the array if necessary
- With the array in its given state, we can then begin deserializing as follows:
  - Create the root with val set to arr[0].
  - Begin a recursive function that takes a node and an index.
    - Calculate 2*idx+1.
      - If it index exceeds the length of the array, skip it.
      - If not, get the element at that index in the array, create a new node, and set its value to it.
      Then recurse with that node and the index
    - Do the same thing for 2*idx+2.
  - At the end, return our newly constructed tree.

- The above functions will take O(n) time for n nodes in the tree. However, if given a linked list, they could
end up producing a tremendous amount of waste; assuming the root is at depth 0,there are (2^n)+1 nodes in a
binary tree of depth n; if we created a linked list that is 10 nodes long, then the array approach would, at minimum,
require (2^9)+2 or 514 units. However, because our dynamic array resize will allocate memory by doubling when insufficent size
exists, we will wind up allocating size equal to the nearest power of 2 greater than the index of our deepest element, therefore
to accomdate our linked list of 10 nodes, we wind up allocating a whopping 1024-unit array.
"""
import math
import collections
import random


class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def treeInsert(node, val):
    if val < node.val:
        if node.left:
            treeInsert(node.left, val)
        else:
            node.left = TreeNode(val)
    elif val > node.val:
        if node.right:
            treeInsert(node.right, val)
        else:
            node.right = TreeNode(val)


def createBst(size, randomize=True):
    if size < 1:
        return
    root = TreeNode(0)
    for val in range(1, size + 1):
        if randomize:
            val = random.randint(-100, 100)
        treeInsert(root, val)
    return root


def levelOrderTraversal(root):
    q = collections.deque([root])
    while q:
        curr = q.popleft()
        print(curr.val)
        if curr and curr.left:
            q.append(curr.left)
        if curr and curr.right:
            q.append(curr.right)


class Codec:
    def bfsSerialize(self, root):
        q = collections.deque([root])
        serialString = ''
        while q:
            curr = q.popleft()
            if curr == None:
                serialString += "None,"
            else:
                serialString += str(curr.val) + ","
                q.append(curr.left)
                q.append(curr.right)
        return serialString

    def serialize(self, root):
        if root:
            return self.bfsSerialize(root)

    def dfsDeserialize(self, data, idx):
        if idx >= len(data) or data[idx] == None:
            print("Rejecting idx: {0}".format(idx))
            return None

        node = TreeNode(data[idx])
        print("Node val: {0}, idx: {1}".format(data[idx], idx))
        node.left = self.dfsDeserialize(data, 2*idx+1)
        node.right = self.dfsDeserialize(data, 2*idx+2)
        return node

    def deserialize(self, data):
        if data == None:
            return None
        data = collections.deque([eval(val) for val in data.split(',') if val])
        print(data)
        return self.dfsDeserialize(data, 0)


if __name__ == '__main__':
    c = Codec()
    # t = createBst(10)
    # levelOrderTraversal(t)
    # serialized = c.serialize(t)
    # deserialized = c.deserialize(serialized)
    # print(c.serialize(t))
    # levelOrderTraversal(deserialized)
    levelOrderTraversal(c.deserialize('5,2,3,None,None,2,4,3,1'))
