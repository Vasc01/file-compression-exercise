# Info
File compression program for exercise purpose.

For more information on the project and contribution guidelines see the project Wiki.

# How to Run

- Technical requirements:
  - [python 3.7 or newer](https://www.python.org)
  - [fire CLI library](https://github.com/google/python-fire)
  - [rich text library](https://github.com/Textualize/rich)

 Note: Some terminals may not support visualizations like loading bars and icons. Other than that the encoding and decoding schuldnt be affected.
 
# How to Use

The program is operated from the terminal or the IDE.

Entry point to the program is the varc.py file.

If you start with `C:\path\to\varc.py\file\location> python varc.py` you will receieve listed command options.
Advisable is to start with `C:\path\to\varc.py\file\location> python varc.py -i` or `C:\path\to\varc.py\file\location> python varc.py --info`. This will provide more detailed command formating information as listed bellow.

```
────────────────────────────────────────────── Info ─────────────────────────────────────────────────────────────────────
This application will perform encoding or decoding on any type of files usingeither Huffman or LZW compression algorithm.
It is operated as follows:
command   complete path or file name   algorithm   optional new name for the output file
--encode  filename.extension           lzw/huf     new_filename                         
--decode  filename.extension                       new_filename                         

Examples:
-e text.txt lzw encoded_text
--encode text.txt lzw encoded_text
-d encoded_text.lzw decoded_text
--decode encoded_text.lzw decoded_text
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
```

Commands for encoding decoding and display of the info block are available in long and short version.

| Command      | Shortcut   |
|--------------|------------|
| encode       | `-e`       |
| encode       | `--encode` |
| decode       | `-d`       |
| decode       | `--decode` |
| info         | `-i`       |
| info         | `--info`   |

- For decoding there is no need to state the decoding algorithm. The correct one will be activated from the file extension.
- The new file name desn't need file extension. An extension is given automatically to the compressed file from the compression algorithm and the decompressed file receives its original extension.
- Encoding and decoding are possible on files not placed in the local folder but in any folder. For this to happen a complete path is passed with the file name. For example
  `C:\path\to\varc.py\file\location> python varc.py --encode "C:\Files\uml.png" lzw `.
