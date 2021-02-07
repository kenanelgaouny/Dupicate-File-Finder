from optparse import OptionParser 
import os, sys, hashlib

BLOCKSIZE = 10000

class hasher:
    def __init__(self):
        self._hasher = hashlib.md5()

    def hash_chunk(self, chunk):
        self._hasher.update(chunk)
        return  self._hasher.hexdigest()


def find_same_content(basefile, filelist):
    #print("Comparing %s to %s" % (basefile, str(filelist)))
    matches = set()
    for f in filelist:
        same = True
        bh = hasher()
        ch = hasher()
        with open(f, 'rb') as fc, open(basefile, 'rb') as fb:
            chunkfb = fb.read(BLOCKSIZE)
            while chunkfb:
                chunkfc = fc.read(BLOCKSIZE)
                if not bh.hash_chunk(chunkfb) == ch.hash_chunk(chunkfc):
                    same = False
                    break
                chunkfb = fb.read(BLOCKSIZE)
                chunkfc = fc.read(BLOCKSIZE)
            if same:
                matches.add(f)
    if matches:
        matches.add(basefile)
        #print(matches)
    return matches


def main():
    parser = OptionParser(description="A tool to find duplicate files that have the same content") 

    parser.add_option("-p", "--path", 
                    dest = "basepath", 
                    help = "Path to start the search from") 
    (options, args) = parser.parse_args()

    if not options.basepath:
        print("A base path is required please provide it using -p or --path and try again")
        sys.exit(1)
    if not os.path.isdir(options.basepath):
        print("--path does not exist or is not a directory.")
        sys.exit(1)

    files_found={}
    result={}
    for rt, dr, fl in os.walk(options.basepath):
        for f in fl:
            fpath = os.path.join(rt,f)
            fsize = os.stat(fpath).st_size
            if fsize in files_found:
                matches = find_same_content(fpath, files_found[fsize])
                files_found[fsize].append(fpath)
                if fsize in result:
                    result[fsize].update(matches)
                else:
                    result[fsize] = matches
            else:
                files_found[fsize] = [fpath]
    if result:
        print("Found duplicate files:")
    else:
        print("No duplicates were found")
    for matchset in result.values():
        print(matchset)       

if __name__ == "__main__":
    main()