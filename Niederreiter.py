# -- КРИПТОСИСТЕМА НИДЕРРАЙТЕРА --


# шифрование Нидеррайтера (c = m * H(pub)^T)
def encryptionVectorNiederreiter(inputVector, publicMatrix):
    return multiMatrices([inputVector], transposeMatrix(publicMatrix))[0]


# криптосистема Нидеррайтера
def cryptosystemNiederreiter(inputText):

    r = 2
    t = 1
    checkMatrix = createCheckMatrixHamming(r)

    # вычисляем ключи
    randomMatrix, permutationMatrix = generationPrivateKey(checkMatrix)
    publicCheckMatrix = generationPublicMatrix(randomMatrix, checkMatrix, permutationMatrix)

    print("\nКлючи ")
    print(*publicCheckMatrix, sep='\n')

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
    print('\nЗашифрованный текст\n', *encryptedText, sep='')
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
    print('\nИнформационного вектора e * P^-1')
    print(*decryptedText, sep='')

    # извлечение t информационных бит
    lengthDecryptedText = len(decryptedText)
    for i in range(0, lengthDecryptedText, n):
        outputText += decryptedText[i:i+t]
    print('\nДекодированный текст в bin\n', *outputText, sep='')
    # вырезаем последний информационный блок и добавленные биты
    return outputText[:-convertBinaryToDecimal(outputText[-t:])-t]