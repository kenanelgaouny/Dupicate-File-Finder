from optparse import OptionParser 
import os, sys, hashlib

BLOCKSIZE = 10000

class hasher:
    def __init__(self):
        self._hasher = hashlib.md5()

    def hash_chunk(self, chunk):
        self._hasher.update(chunk)
        return  self._hasher.hexdigest()


def find_same_content(basefile, filelist, bytecmp=False):
    #print("Comparing %s to %s" % (basefile, str(filelist)))
    matches = set()
    for f in filelist:
        same = True
        # hashers are not needed if we're doing by by byte compares
        if not bytecmp:
            basefile_hasher = hasher()
            file_hasher = hasher()
        
        with open(f, 'rb') as fc, open(basefile, 'rb') as fb:
            basefile_chunk = fb.read(BLOCKSIZE)
            while basefile_chunk:
                file_chunk = fc.read(BLOCKSIZE)
                if bytecmp and not (basefile_chunk == file_chunk):
                    same = False
                    break
                elif not bytecmp and not (basefile_hasher.hash_chunk(basefile_chunk) == file_hasher.hash_chunk(file_chunk)):
                    same = False
                    break
                basefile_chunk = fb.read(BLOCKSIZE)
                file_chunk = fc.read(BLOCKSIZE)
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
    parser.add_option("-b", "--compareBytes",
                    dest="byteCompare", 
                    action="store_true",
                    default=False,
                    help="Preform byte by byte comparison instead of md5 hash comparison. used to avoid hash collisions")
    (options, args) = parser.parse_args()

    if not options.basepath:
        print("A base path is required please provide it using -p or --path and try again")
        sys.exit(1)
    if not os.path.isdir(options.basepath):
        print("--path does not exist or is not a directory.")
        sys.exit(1)
    if options.byteCompare:
        print("--byte-compare is set wil perform byte by byte comparisons")
    files_found={}
    result={}
    for rt, dr, fl in os.walk(options.basepath):
        for f in fl:
            fpath = os.path.join(rt,f)
            fsize = os.stat(fpath).st_size
            if fsize in files_found:
                matches = find_same_content(fpath, files_found[fsize], options.byteCompare)
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