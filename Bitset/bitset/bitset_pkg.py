#============================================================
#                    Bitset Class
#                       31 August 2019
#============================================================
# A module meant to collect useful functions

import copy, pkg_resources, platform, math

system_name = platform.system()
if system_name != 'Linux':
    __all__=['__doc__','__version__','bitset']
else: # allow the possibility of including the accelerate decorator
    __all__=['__doc__','__version__','bitset']

def get_Docstring(dname):
    with open(pkg_resources.resource_filename('bitset','DocStrings/'+dname),'r') as f:
        s = f.read()
    return s

# __doc__=get_Docstring('ModuleDoc.txt')
# __version__=pkg_resources.get_distribution('bitset').version

#========================================
#            Bitset Class
#========================================

class bitset:
    def __init__(self,length):
        self.__length = length
        self.__bitarr = 1<<self.__length

    def set(self,key=None): # TODO handle slices with negatives
        if key is None:
            self.__bitarr = (1<<(self.__length+1))-1
            return

        if hasattr(key,'__len__'):
            # first check no duplicates
            assert len(set(key))==len(key), 'List of indices must not contain duplicates'
            assert (max(key)<self.__length)&(min(key)>=0), 'Index out of range'
            self.__bitarr |= sum([1<<i for i in key])
            return

        if type(key)==slice:
            start, stop, step = key.start, key.stop, key.step
            if (stop is None)|(stop==-1):
                stop = self.__length
            if start is None:
                start = 0
            if step is None:
                step = 1
            assert stop>=start, 'Stop must be greater than start'
            assert (stop>=0)&(start>=0), 'Start and stop must be positive'
            assert step>0, 'Step must be positive'
            assert (start>=0)&(stop<=self.__length), 'Index out of range'
            self.__bitarr |= sum([1<<i for i in range(start, stop, step)])
            return

        assert (key<self.__length)&(key>=0), 'Index out of range'
        self.__bitarr |= 1<<key


    def reset(self,key=None):
        if key is None:
            self.__bitarr = 1<<self.__length
            return

        if hasattr(key,'__len__'):
            # first check no duplicates
            assert len(set(key))==len(key), 'List of indices must not contain duplicates'
            assert (max(key)<self.__length)&(min(key)>=0), 'Index out of range'
            self.__bitarr &= (sum([1<<i for i in key])^((1<<(self.__length+1))-1))
            return

        if type(key)==slice:
            start, stop, step = key.start, key.stop, key.step
            if (stop is None)|(stop==-1):
                stop = self.__length
            if start is None:
                start = 0
            if step is None:
                step = 1
            assert stop>=start, 'Stop must be greater than start'
            assert (stop>=0)&(start>=0), 'Start and stop must be positive'
            assert step>0, 'Step must be positive'
            assert (start>=0)&(stop<=self.__length), 'Index out of range'
            self.__bitarr &= (sum([1<<i for i in range(start, stop, step)])^((1<<(self.__length+1))-1))
            return

        assert (key<self.__length)&(key>=0), 'Index out of range'
        self.__bitarr &= ((1<<key)^((1<<(self.__length+1))-1))


    def flip(self,key=None):
        if key is None:
            self.__bitarr ^= (1<<self.__length)-1
            return

        if hasattr(key,'__len__'):
            # first check no duplicates
            assert len(set(key))==len(key), 'List of indices must not contain duplicates'
            assert (max(key)<self.__length)&(min(key)>=0), 'Index out of range'
            self.__bitarr ^= sum([1<<i for i in key])
            return

        if type(key)==slice:
            start, stop, step = key.start, key.stop, key.step
            if (stop is None)|(stop==-1):
                stop = self.__length
            if start is None:
                start = 0
            if step is None:
                step = 1
            assert stop>=start, 'Stop must be greater than start'
            assert (stop>=0)&(start>=0), 'Start and stop must be positive'
            assert step>0, 'Step must be positive'
            assert (start>=0)&(stop<=self.__length), 'Index out of range'
            self.__bitarr ^= sum([1<<i for i in range(start, stop, step)])
            return

        assert (key<self.__length)&(key>=0), 'Index out of range'
        self.__bitarr ^= 1<<key

    def __str__(self):
        return bin(self.__bitarr)[3:]

    def __repr__(self):
        return str(self)

    def __len__(self):
        return self.__bitarr.bit_length()-1


    def __getitem__(self,key):
        assert (type(key)==int)|(type(key)==list)|(type(key)==slice), 'Key must be an int or list of ints'

        if hasattr(key,'__len__'):
            assert (max(key)<self.__length)&(min(key)>=0), 'Index out of range'
            return list((self.__bitarr>>i)&1 for i in key)

        if type(key)==slice:
            start, stop, step = key.start, key.stop, key.step
            if (stop is None)|(stop==-1):
                stop = self.__length
            if start is None:
                start = 0
            if step is None:
                step = 1
            assert (start>=0)&(stop<=self.__length), 'Index out of range'
            return list((self.__bitarr>>i)&1 for i in range(start, stop, step))

        assert (key<self.__length)&(key>=0), 'Index out of range'
        return (self.__bitarr>>key)&1


    def __setitem__(self,key,item):
        assert (type(key)==int)|(type(key)==list)|(type(key)==slice), 'Key must be int or list of ints'
        assert ((type(item)==int)&((item==0)|(item==1)))|(type(item)==list), 'Item must be 0 or 1'

        if hasattr(item,'__len__'):
            assert (set(item)==set([0,1]))|(set(item)==set([0]))|(set(item)==set([1])), 'Item must be list consisting of only 0 and 1'
            assert (type(key)==list)|(type(key)==slice), 'Key/ Item length mismatch'
            if type(key)==list:
                assert len(set(key))==len(key), 'Key contains duplicates'
                assert len(item)==len(key), 'Key/ Item length mismatch'
                assert (max(key)<self.__length)&(min(key)>=0), 'Index out of range'
                for k, i in zip(key,item):
                    if i:
                        self.set(k)
                    else:
                        self.reset(k)
                return
            if type(key)==slice:
                start, stop, step = key.start, key.stop, key.step
                if (stop is None)|(stop==-1):
                    stop = self.__length
                if start is None:
                    start = 0
                if step is None:
                    step = 1
                assert stop>=start, 'Stop must be greater than start'
                assert (stop>=0)&(start>=0), 'Start and stop must be positive'
                assert step>0, 'Step must be positive'
                assert len(item)==math.ceil((stop-start)/step), 'Key/ Item length mismatch'
                assert (start>=0)&(stop<=self.__length), 'Index out of range'
                for k, i in zip(range(start, stop, step),item):
                    if i:
                        self.set(k)
                    else:
                        self.reset(k)
                return

        if item:
            self.set(key)
        else:
            self.reset(key)

        # TODO make this work
        # def __invert__(self):
        #     temp = bitset(self.__length)
        #     temp._bitset__bitarr = self.__bitarr
        #     temp.flip()
        #     return temp

bitset.__doc__=get_Docstring('BitsetDoc.txt')
