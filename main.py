from common import convertDecimalToBinary, convertBinaryToDecimal
from Niederreiter import cryptosystemNiederreiter
import tkinter as tk
from tkinter import messagebox
import sys
from common import *
from generationKeys import *
from HammingCode import *


root=tk.Tk()

# шифрование Нидеррайтера (c = m * H(pub)^T)
def encryptionVectorNiederreiter(inputVector, publicMatrix):
    return multiMatrices([inputVector], transposeMatrix(publicMatrix))[0]


# криптосистема Нидеррайтера
def cryptosystemNiederreiter(inputText):

    r = 3
    t = 1
    checkMatrix = createCheckMatrixHamming(r)

    # вычисляем ключи
    randomMatrix, permutationMatrix = generationPrivateKey(checkMatrix)
    publicCheckMatrix = generationPublicMatrix(randomMatrix, checkMatrix, permutationMatrix)

    print("\nКлючи ")
    print(*publicCheckMatrix, sep='\n')
    keys.insert(0, publicCheckMatrix)

    n = len(checkMatrix[0])
    nk = len(checkMatrix)
    # увеличение размера текста до длины кратной t
    inputText = addSize(inputText, t)
    # шифрование вектора
    lengthInputText = len(inputText)
    encryptedText = []
    for i in range(0, lengthInputText, t):
        # формируем вектор весом t
        inputVector = [0] * n
        for j in range(t):
            inputVector[j] = inputText[i+j]
        encryptedText.extend(encryptionVectorNiederreiter(inputVector, publicCheckMatrix))
    print('\nЗакодированный текст\n', *encryptedText, sep='')
    encrypted.insert(0, encryptedText)
    
    # дешифрование вектора

    lengthEncryptedText = len(encryptedText)
    outputText = []
    decryptedText = []

    for i in range(0, lengthEncryptedText, nk):
        # вычисление синдрома s = c * (S^T)^-1
        syndrome = multiMatrices([encryptedText[i:i+nk]], reverseMatrix(transposeMatrix(randomMatrix)))[0]
        errorVector = [0] * len(permutationMatrix)
        index = convertBinaryToDecimal(syndrome)
        if index != 0:
            errorVector[index - 1] = 1
        
        # получение информационного вектора e * P^-1
        decryptedText.extend(multiMatrices([errorVector], reverseMatrix(transposeMatrix(permutationMatrix)))[0])
    #resultsyndrome.insert(0, errorVector)
    resultvectore.insert(0, decryptedText)
        

        

    # извлечение t информационных бит
    lengthDecryptedText = len(decryptedText)
    for i in range(0, lengthDecryptedText, n):
        outputText += decryptedText[i:i+t]
    print('\nДекодированный текст в bin\n', *outputText, sep='')
    # вырезаем последний информационный блок и добавленные биты
    return outputText[:-convertBinaryToDecimal(outputText[-t:])-t]



def encode():

    resultbin.delete(0, 99999)

    keys.delete(0, 99999)
    #resultsyndrome.delete(0, 99999)
    resultvectore.delete(0, 99999)

    
    inputText = entermessage.get()
    print(inputText)
    # первод текста в бинарный вектор
    binText = []
    for symbol in inputText:
        binText.extend(convertDecimalToBinary(ord(symbol), 8))

    print('\nКод Хемминга')

    binDecryptedText = cryptosystemNiederreiter(binText)
    resultbin.insert(0, binDecryptedText)

    # перевод бинарного вектора в символьный текст
    lengthDecryptedText = len(binDecryptedText)
    outputText = ''
    for i in range(0, lengthDecryptedText, 8):
        outputText += chr(convertBinaryToDecimal(binDecryptedText[i:i+8]))
    result10.delete(0, 99999)
    result10.insert(0, outputText)

    print('\nДекодированный текст\n', outputText)



def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()
        






root.eval('tk::PlaceWindow . center')
root.title("Niederreiter Cryptosystem")
root.configure(bg="black")
root.geometry('500x500')


bttn = tk.Button(root, text="Encode", width = 25, borderwidth=3, font= 'Consolas 10', fg="Grey", bg="black", command = encode)
bttn.pack(pady= 10)


entermessage = tk.Entry(root, text="Enter text here", width = 25, borderwidth=1, font= 'Consolas 10', fg="Grey", bg="black", justify='center')
entermessage.pack(pady= 10)

label2 = tk.Label(text="Encoded", fg="Grey", bg="black")
label2.pack()

encrypted = tk.Entry(root, width = 25, borderwidth=1, font= 'Consolas 10', fg="Grey", bg="black", justify='center')
encrypted.pack(pady=5)

label2 = tk.Label(text="Public Keys", fg="Grey", bg="black")
label2.pack()

keys = tk.Entry(root, width = 25, borderwidth=1, font= 'Consolas 10', fg="Grey", bg="black", justify='center')
keys.pack(pady=5)

""" label2 = tk.Label(text="Syndrome", fg="Grey", bg="black")
label2.pack()

resultsyndrome = tk.Entry(root, width = 25, borderwidth=1, font= 'Consolas 10', fg="Grey", bg="black", justify='center')
resultsyndrome.pack(pady=5) """

label2 = tk.Label(text="Vector e", fg="Grey", bg="black")
label2.pack()

resultvectore = tk.Entry(root, width = 25, borderwidth=1, font= 'Consolas 10', fg="Grey", bg="black", justify='center')
resultvectore.pack(pady=5)





label1 = tk.Label(text="Decoded", fg="Grey", bg="black")
label1.pack()

resultbin = tk.Entry(root, width = 25, borderwidth=1, font= 'Consolas 10', fg="Grey", bg="black", justify='center')
resultbin.pack(pady= 5)

result10 = tk.Entry(root, width = 25, borderwidth=1, font= 'Consolas 10', fg="Grey", bg="black", justify='center')
result10.pack(pady=5)







root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
sys.exit()