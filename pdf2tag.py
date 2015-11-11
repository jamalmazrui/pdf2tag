# pdf2tag
# Version 1.0
# Adapted from the py2txt.py utility that is included with the Python module called PDFMiner

#!C:\Python27\python2.7.exe
import sys
import os
import glob
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice, TagExtractor
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.cmapdb import CMapDB
from pdfminer.layout import LAParams
from pdfminer.image import ImageWriter

# main
def main(argv):
    import getopt
    def usage():
        print 'Syntax:\npdf2htm.exe SourcePDF\n where the parameter is either a file name or\na wildcard spec like\n*.pdf\nEnclose it with quotes if it contains a space\n\nAdditional options are supported with named command line parameters as follows:'
        print ('usage: %s [-d] [-p pagenos] [-m maxpages] [-P password] [-o output]'
               ' [-C] [-n] [-A] [-V] [-M char_margin] [-L line_margin] [-W word_margin]'
               ' [-F boxes_flow] [-Y layout_mode] [-O output_dir] [-R rotation]'
               ' [-t text|html|xml|tag] [-c codec] [-s scale]'
               ' file ...' % argv[0])
        return 100
    try:
        (opts, args) = getopt.getopt(argv[1:], 'dp:m:P:o:CnAVM:L:W:F:Y:O:R:t:c:s:')
    except getopt.GetoptError:
        return usage()
    if not args: return usage()
    # debug option
    debug = 0
    # input option
    password = ''
    pagenos = set()
    maxpages = 0
    # output option
    outfile = None
    outtype = 'tag'
    imagewriter = None
    rotation = 0
    layoutmode = 'normal'
    codec = 'utf-8'
    pageno = 1
    scale = 1
    caching = True
    showpageno = False
    laparams = LAParams()
    for (k, v) in opts:
        if k == '-d': debug += 1
        elif k == '-p': pagenos.update( int(x)-1 for x in v.split(',') )
        elif k == '-m': maxpages = int(v)
        elif k == '-P': password = v
        elif k == '-o': outfile = v
        elif k == '-C': caching = False
        elif k == '-n': laparams = None
        elif k == '-A': laparams.all_texts = True
        elif k == '-V': laparams.detect_vertical = True
        elif k == '-M': laparams.char_margin = float(v)
        elif k == '-L': laparams.line_margin = float(v)
        elif k == '-W': laparams.word_margin = float(v)
        elif k == '-F': laparams.boxes_flow = float(v)
        elif k == '-Y': layoutmode = v
        elif k == '-O': imagewriter = ImageWriter(v)
        elif k == '-R': rotation = int(v)
        elif k == '-t': outtype = v
        elif k == '-c': codec = v
        elif k == '-s': scale = float(v)
    #
    PDFDocument.debug = debug
    PDFParser.debug = debug
    CMapDB.debug = debug
    PDFResourceManager.debug = debug
    PDFPageInterpreter.debug = debug
    PDFDevice.debug = debug
    #
    rsrcmgr = PDFResourceManager(caching=caching)
    if not outtype:
        outtype = 'tag'
        if outfile:
            if outfile.endswith('.htm') or outfile.endswith('.html'):
                outtype = 'html'
            elif outfile.endswith('.xml'):
                outtype = 'xml'
            elif outfile.endswith('.tag'):
                outtype = 'tag'
    if outfile:
        outfp = file(outfile, 'w')
    else:
        outfp = sys.stdout

    for fname in args:
        l = glob.glob(fname)
        count = len(l)
        print 'Converting ' + str(count) + ' from ' + fname + ' to ' + outtype + ' format'
        for pdf in l:
#             print pdf
            d = {'html' : 'htm', 'tag' : 'tag', 'text' : 'txt', 'xml' : 'xml'}
            ext = '.' + d[outtype]
            outfile = pdf[0:-4] + ext
            print outfile
            outfp = file(outfile, 'wb')
            if outtype == 'text':
                device = TextConverter(rsrcmgr, outfp, codec=codec, laparams=laparams,
                                       imagewriter=imagewriter)
                device.showpageno = False
            elif outtype == 'xml':
                device = XMLConverter(rsrcmgr, outfp, codec=codec, laparams=laparams,
                                      imagewriter=imagewriter)
                device.showpageno = False
            elif outtype == 'html':
                device = HTMLConverter(rsrcmgr, outfp, codec=codec, scale=scale,
                                       layoutmode=layoutmode, laparams=laparams,
                                       imagewriter=imagewriter)
                device.showpageno = False
            elif outtype == 'tag':
                device = TagExtractor(rsrcmgr, outfp, codec=codec)
                device.showpageno = False
            else:
                return usage()
    
            fp = file(pdf, 'rb')
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            for page in PDFPage.get_pages(fp, pagenos,
                                          maxpages=maxpages, password=password,
                                          caching=caching, check_extractable=True):
                page.rotate = (page.rotate+rotation) % 360
                interpreter.process_page(page)
            fp.close()
            device.close()
            outfp.close()

        print 'Done'
    return

if __name__ == '__main__': sys.exit(main(sys.argv))
