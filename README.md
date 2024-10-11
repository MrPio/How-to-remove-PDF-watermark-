# How do you remove watermarks from PDF files?
This repository shows the result of my recent attempt to remove an annoying watermark that the professor placed over each page of the slides. I didn't really want to print them along with the watermark.

<p align="center">
  <img src="https://github.com/user-attachments/assets/8936eccc-883b-428a-812f-a40c81600c13" width="750rem"/>
</p>
⚠️ *Disclaimer*: The contents of this repository are for informational purposes only. I do not intend to publish any copyright-infringing content.

## 🌊 Types of watermark
Watermarks in PDFs can be applied mainly in two ways:
- *As a separate overlay or image*: The watermark is added as an overlay over the PDF content.
- *Embedded within the content*: The watermark is embedded directly into the text or image layers, making them harder to remove.

If the watermark is an overlay, it can potentially be removed using PDF editing tools like [`pdftk`](https://www.pdflabs.com/tools/pdftk-the-pdf-toolkit/), [`qpdf`](https://github.com/qpdf/qpdf), [`pdfcpu`](https://pdfcpu.io/core/watermark.html), or graphical tools like [`LibreOffice Draw`](https://www.libreoffice.org/discover/draw/).

## ❌ Remove the watermark
Let's review some methods to remove the watermark.

### 🛠️ [1/3] Using automated tools
You should check if the following does the job:
```[bash]
$ pdfcpu watermark remove [-p(ages) selectedPages] inFile [outFile]
```

### 🎨 [2/3] Replacing the colour of the watermark 
One easy-to-go strategy is:
1. Rasterize the PDF into *JPG* or *PNG* images, using one of the many online/offline tools,
2. Sample the watermark colour with `Paint`, `GIMP` or similar tools.
3. Use a tool like [`XnView`](https://www.xnview.com/en/xnview/) to bulk replace the watermark colour with the background colour, with a small **tolerance**, for all the page images,
4. Merge the images back into a PDF using one of the many online/offline tools.

Although this is a very simple technique, **it only works if the watermark is placed behind the content, not as a semi-transparent stamp on top of the content**. In the latter case, there wouldn't be a consistent colour for the watermark, and even increasing the tolerance would affect the PDF content.

Another drawback of this method is that we lose information when rasterising the PDF in point 1. This means, for example, that **the text in the resulting PDF can no longer be selected or copied**.

### 🔧 [3/3] The manual approach
If automated tools don't remove the watermark, you have to manually analyse the PDF content and identify the *object* responsible for the watermark.

#### 📂 [Optional] Uncompress the PDF
First and foremost, you could *uncompress* the PDF to improve the readability of the text, undoing the flate, ZIP or other PDF compressions. This can be achieved with one of the following commands:
```[bash]
$ qpdf --qdf --object-streams=disable inFile [outFile]
$ pdftk inFile output outFile uncompress
```
#### 🔍 Identify the watermark object
A PDF object is structured as follows:

```[pdf]
<object_id> 0 obj
  <<
    /ColorSpace 9 0 R
    /ShadingType 2
    ...
  >>
endobj
```

We need to identify the watermark `obj` and replace its content with the empty dictionary `<< >>`. 

This part is trial and error, but we are not going to go blind as there are tricks that can be used:
1. Work on a 1-page sample, possibly a page without images or other large binary objects, to get a clearer view of the PDF structure and identify the watermark more quickly,
2. The string "watermark" or the actual watermark content may appear in the uncompressed version of the PDF,
3. A watermark usually has a wide width and a high height. In my case, the entries `/Width 720` and `/Height 540` identified the watermark.

In my case, the culprit was the following:
<p align="center">
  <img src="https://github.com/user-attachments/assets/b46b46e4-cbe0-419b-8228-68b4b66405a2" width="650rem"/>
</p>

In my experience, if you try to edit the PDF content with text editors like *VSC*, *nano*, *Mousepad* etc..., the file gets corrupted, probably due to the wrong text encoding the editor inferred on a binary file like the PDF. The only text editor I found that doesn't change the file encoding was *Vim*.

#### ✂️ Batch clean multiple PDF files

You could either use `Vim`, `sed` or related tools to manually patch the PDFs, or use a Python script to automate the job.

I have attached two scripts to this repository:
- [**cleaner.py**](/cleaner.py) - Patch all the PDF files in the CWD. **Before launching the script be sure to have placed the entries for your watermark found in the previous step inside the `watermark_features` list**. This script uses the regular expression `<<[^>]+>>` to identify all the PDF dictionaries, i.e. object arguments, and filter them by keeping only those having all the watermark features.
- [**unlocker.py**](/unlocker.py) - Unlock all the permission for all the PDF files in the CWD. This requires `pdftk` to work.

#### 🔥 Test the result
If you've got this far, you should see some results. However, as in my case, different PDF files had slightly different watermark objects, so I reran the script several times with different `watermark_features` values for those files.
I also happened to find a file where the watermark object couldn't be removed without corrupting the whole file. What I did was to set the `/Width` property to `0` instead of removing the object.
