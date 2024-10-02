# redis_fuse.py
import os
import redis
import fuse

class RedisFS(fuse.Operations):
    def __init__(self, redis_host='localhost', redis_port=6379):
        self.r = redis.Redis(host=redis_host, port=redis_port)

    def readdir(self, path, fh):
        keys = self.r.keys('*')
        files = [key.decode('utf-8') for key in keys]
        return ['.', '..'] + files

    def getattr(self, path, fh=None):
        if path == "/" or path == ".":
            st = os.lstat(".")
            return dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime', 'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))
        else:
            key = path.lstrip("/")
            if self.r.exists(key):
                size = self.r.strlen(key)
                return {'st_atime': 0, 'st_ctime': 0, 'st_gid': 0, 'st_mode': 0o100644, 'st_mtime': 0, 'st_nlink': 1, 'st_size': size, 'st_uid': os.getuid()}
            else:
                raise fuse.FuseOSError(fuse.errno.ENOENT)

    def open(self, path, flags):
        return 0

    def read(self, path, size, offset, fh):
        key = path.lstrip("/")
        if self.r.exists(key):
            data = self.r.get(key)
            return data[offset:offset + size]
        else:
            raise fuse.FuseOSError(fuse.errno.ENOENT)

    def write(self, path, data, offset, fh):
        key = path.lstrip("/")
        self.r.set(key, data)
        return len(data)

    def create(self, path, mode):
        key = path.lstrip("/")
        self.r.set(key, "")
        return 0

    def unlink(self, path):
        key = path.lstrip("/")
        if self.r.exists(key):
            self.r.delete(key)
        else:
            raise fuse.FuseOSError(fuse.errno.ENOENT)

if __name__ == '__main__':
    fuse = fuse.FUSE(RedisFS(), '/mnt/redis', foreground=True)
