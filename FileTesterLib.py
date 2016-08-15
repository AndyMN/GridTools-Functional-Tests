import hashlib


class FileTesterLib:


    def __init__(self):
        pass


    def _generate_file_hash(self, file_name, hash_type="md5"):
        hash_boy = None

        if hash_type == "md5":
            hash_boy = hashlib.md5()
        elif hash_type == "sha1":
            hash_boy = hashlib.sha1()
        elif hash_type == "sha224":
            hash_boy = hashlib.sha224()
        elif hash_type == "sha256":
            hash_boy = hashlib.sha256()
        elif hash_type == "sha384":
            hash_boy = hashlib.sha384()
        elif hash_type == "sha512":
            hash_boy = hashlib.sha512
        else:
            try:
                hash_boy = hashlib.new(hash_type)
            except:
                raise ValueError("No hash algorithm available for: " + hash_type)

        if hash_boy:
            with open(file_name, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), ""):
                    hash_boy.update(chunk)

            return hash_boy.hexdigest()
        else:
            raise TypeError("Hash maker is NoneType")

    def files_should_be_the_same(self, file1_name, file2_name, hash_type="md5"):
        hash_file1 = self._generate_file_hash(file1_name, hash_type=hash_type)
        hash_file2 = self._generate_file_hash(file2_name, hash_type=hash_type)

        if hash_file1 != hash_file2:
            raise AssertionError("Hashes don't match ! Files don't contain the same data !")
        else:
            print "Files are the same !"
            print hash_type + ": " + hash_file1