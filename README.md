# Code for the article "A Computational Approach to Literary Value in North Korea"


This repository contains the Python code used for the different sections of the article:

- `decryption` : decrypt the xor-encrypted PDF files extracted from KLM Viewer. Running `python decrypt.py` in the folder where the PDF files are stored will automatically decrypt and save a clear version of the PDFs in the same folder.
- `split_choson_munhak_pdfs` : parse the index of the PDF files and automatically extract, for each issue, the pages containing short stories (단편소설). The filtering can be modified to parse and extract all articles separately
- `language_model_training` : expand the vocabulary of KoBERT to include a North Korean lexicon and fine-tune it on a masked language modeling task using a corpus of North Korean data.
- `notebooks` : Jupyter notebooks with the code for the text mining analysis and "originality scoring" used in the paper, as well as to produce the different data visualizations.