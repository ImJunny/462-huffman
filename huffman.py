# NODE class
class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

def buildFrequencyTable(textFile):
    frequency = {}
    with open(textFile, 'r') as file:
        text = file.read()
        for char in text:
            if char.isalpha():
                if char in frequency:
                    frequency[char] += 1
                else:
                    frequency[char] = 1
    return frequency

def heapify(priorityQueue, index):
    smallest = index
    left_child = 2 * index + 1
    right_child = 2 * index + 2
    if left_child < len(priorityQueue) and priorityQueue[left_child][0] < priorityQueue[smallest][0]:
        smallest = left_child
    if right_child < len(priorityQueue) and priorityQueue[right_child][0] < priorityQueue[smallest][0]:
        smallest = right_child
    if smallest != index:
        priorityQueue[index], priorityQueue[smallest] = priorityQueue[smallest], priorityQueue[index]
        heapify(priorityQueue, smallest)

def buildPriorityQueue(frequency):
    priorityQueue = [(freq, Node(char, freq)) for char, freq in frequency.items()]
    for i in range(len(priorityQueue) // 2 - 1, -1, -1):
        heapify(priorityQueue, i)
    return priorityQueue

def extractMin(priorityQueue):
    if not priorityQueue:
        return None
    min_element = priorityQueue[0]
    priorityQueue[0] = priorityQueue[-1]
    priorityQueue.pop()
    heapify(priorityQueue, 0)
    return min_element

def buildHuffmanTree(priorityQueue):
    while len(priorityQueue) > 1:
        left_freq, left_node = extractMin(priorityQueue)
        right_freq, right_node = extractMin(priorityQueue)
        parent = Node(None, left_freq + right_freq)
        parent.left = left_node
        parent.right = right_node
        priorityQueue.append((parent.freq, parent))
        for i in range(len(priorityQueue) // 2 - 1, -1, -1):
            heapify(priorityQueue, i)
    return priorityQueue[0][1]

def buildCodesTable(root):
    codes = {}
    def traverse(node, code=""):
        if node.char:
            codes[node.char] = code
        else:
            traverse(node.left, code + "0")
            traverse(node.right, code + "1")
    traverse(root)
    return codes

def encodeText(text, codes):
    encodedText = ""
    for char in text:
        if char.isalpha():
            encodedText += codes[char]
    return encodedText

# MAIN
if __name__ == "__main__":
    textFile = "huffman_coding_text.txt"
    frequency = buildFrequencyTable(textFile)
    priorityQueue = buildPriorityQueue(frequency)
    huffmanTree = buildHuffmanTree(priorityQueue)
    codes = buildCodesTable(huffmanTree)

    # originalSize = sum of each character * 8 (each character is 8 bits)
    originalSize = 0
    for char in frequency.keys():
        originalSize+=frequency[char]*8
    # compressedSize = sum of each character * length of each code
    compressedSize = 0
    text=open(textFile).read()
    for char in text:
        if char.isalpha():
            compressedSize+=len(codes[char])

    # output data
    print("Frequency Table:")
    for char, freq in frequency.items():
        print(f"{char}: {freq}")
    print("\nCharacter Codes:")
    for char, code in codes.items():
        print(f"{char}: {code}")
    print("\nOriginal Size:", originalSize)
    print("Compressed Size:", compressedSize)
    print("Compression Ratio:", compressedSize / originalSize)