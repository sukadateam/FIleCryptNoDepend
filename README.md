# FIleCryptNoDepend
Simple File Encryption with no dependencies!

A finished project! 

* Might add multi level scrambling. Where instead of it only running once, it's runs several of times over, each time with different keys.
* Password lock to tax_returns.txt might be added.

Uses basic logic to encrypt files. Documenation will be made about how it works.

DO NOT DECRYPT A FILE THAT'S NOT ENCRYPTED. YOU CANNOT DECRYPT IT AFTERWARDS, EVEN IF YOU INSTEAD DID ENCRYPT.

Command Line Logic:
  * -e, -E \<file> = Encrypt File, Searches for tax_returns.txt
  * -d, -D \<file> = Decrypt File, Searches for tax_returns.txt
  * -k, -K \<key> = Specify the key to decrypt the file. Known as "taxHash" var inside of tax_returns.txt

Examples:
  * python Code_Discovery.py -e "filepath"
  * python Code_Discovery.py -e "filepath" -k "e3nd45k0sd0mcouiaupw2jf3ag2iyk1h0pj04hkb5zjemibeij"

Currently, If you forget the key. There is no way to recover the data. I'm not planning on making a program to do this either as it elimites the point of this.
