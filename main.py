from common import convertDecimalToBinary, convertBinaryToDecimal
from Niederreiter import cryptosystemNiederreiter


inputText = input("Введите текс: ")
# перевод текста в бинарный вектор
binText = []
for symbol in inputText:
    binText.extend(convertDecimalToBinary(ord(symbol), 8))

print('\nКод Хемминга')

binDecryptedText = cryptosystemNiederreiter(binText)

# перевод бинарного вектора в символьный текст
lengthDecryptedText = len(binDecryptedText)
outputText = ''
for i in range(0, lengthDecryptedText, 8):
    outputText += chr(convertBinaryToDecimal(binDecryptedText[i:i+8]))

print('Раскодированный текст:', outputText)
