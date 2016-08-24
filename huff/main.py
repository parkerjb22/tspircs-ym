from compressor import Compressor
from decompressor import Decompressor

inputFileName = 'debug.txt'
compressedFileName = 'compress.zip'
decompressedFileName = 'uncompress.txt'

Compressor(inputFileName, compressedFileName).run()
Decompressor(compressedFileName, decompressedFileName).run()