//Jiuzhang
//1. Linear Data Structure: Queue & Stack & Hash
***************************************
//1.1 Happy Number
/** Happy number: 19
    1^2 + 9^2 = 82
    9^2 + 2^2 = 68
    6^2 + 8^2 = 100
    1^2 + 0^2 + 0^2 = 1
*/
***************************************
//1.2 Min Stack: push / pop / getMin
push: 
    /** If x will be the new min
     * push old min, then change min to x
     * then push x
     * E.G. [-2,0,4,-3,2,-4,5] --> [MAX(old),-2,0,4,-2(old),-3,2,-3(old),-4(new),5]
     */
pop:
    /** If we pop the min element
     * we need to pop twice 
     * then set the second pop as min
     * E.G. when pop(-4), min=-4 --> pop(-3) --> min=-3 --> [MAX,-2,0,4,-2,-3,2]
     */
***************************************
//1.3 Inplement Queue Using Stacks
//1.4 Inplement Stack Using Queues
***************************************
//1.5 Largest Rectangle In Histogram
***************************************
//1.6 Rehashing
//enlarge the hash table
public class Solution {
    /**
     * @param hashTable: A list of The first node of linked list
     * @return: A list of The first node of linked list which have twice size
     */
    public ListNode[] rehashing(ListNode[] hashTable) {
        // write your code here
        if (hashTable.length <= 0) {
            return hashTable;
        }
        int newcapacity = 2 * hashTable.length;
        ListNode[] newTable = new ListNode[newcapacity];
        for (int i = 0; i < hashTable.length; i++) {
            while (hashTable[i] != null) {
                int newindex
                 = (hashTable[i].val % newcapacity + newcapacity) % newcapacity;
                if (newTable[newindex] == null) {
                    newTable[newindex] = new ListNode(hashTable[i].val);
                   // newTable[newindex].next = null;
                } 
                else {
                    ListNode dummy = newTable[newindex];
                    while (dummy.next != null) {
                        dummy = dummy.next;
                    }
                    dummy.next = new ListNode(hashTable[i].val);
                }
                hashTable[i] = hashTable[i].next;
            }
        }
        return newTable;
    }
}
***************************************
//1.7 Thread Safe
HashTable: Safe
HashSet: Not Safe
HashMap: Not Safe
***************************************
//1.8 LeastRecentlyUsed Cache
/** e.g. [2,1,3,2,5,3,6,7], we can only store 3 numbers
* Node: key, value, prev, next
* 2 -> 1 -> 3 
* then visit 2 : 1 -> 3 -> 2
* 3 -> 2 -> 5
* 2 -> 5 -> 3
* when visit again: delete it then add it at tail
*/
public class LRUCache {
    private class Node{
        Node prev;
        Node next;
        int key;
        int value;

        public Node(int key, int value) {
            this.key = key;
            this.value = value;
            this.prev = null;
            this.next = null;
        }
    }

    private int capacity;
    private HashMap<Integer, Node> hs = new HashMap<Integer, Node>();
    private Node head = new Node(-1, -1);
    private Node tail = new Node(-1, -1);

    public LRUCache(int capacity) {
        this.capacity = capacity;
        tail.prev = head;
        head.next = tail;
    }

    public int get(int key) {
        if( !hs.containsKey(key)) {
            return -1;
        }

        // remove current
        Node current = hs.get(key);
        current.prev.next = current.next;
        current.next.prev = current.prev;

        // move current to tail
        move_to_tail(current);

        return hs.get(key).value;
    }

    public void set(int key, int value) {
        if( get(key) != -1) {
            hs.get(key).value = value;
            return;
        }

        if (hs.size() == capacity) {
            hs.remove(head.next.key);
            head.next = head.next.next;
            head.next.prev = head;
        }

        Node insert = new Node(key, value);
        hs.put(key, insert);
        move_to_tail(insert);
    }

    private void move_to_tail(Node current) {
        current.prev = tail.prev;
        tail.prev = current;
        current.prev.next = current;
        current.next = tail;
    }
}

//2. Tree Data Structure: Heap
add()
poll() //remove min 
