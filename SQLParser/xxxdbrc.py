import sys
import os
import re

recomment = re.compile(r'^[ \t]*(#.*)*$')
class config(dict):

    def __init__(self, prefix, debug=True, rw=False, name=None):
        dict.__init__(self, (
            ('hostname', None),
            ('username', 'daqread'),
            ('password', 'daqread'),
            ('dbname', prefix+'dbase'),
            ('port', 0),
            ('hostname1', None),
            ('username1', None),
            ('password1', None),
            ('port1',     None),
            ))
        self['rw'] = rw

        if name is None:
            dirs = [ './',
                     '.testrelease/',
                     '.testrelease/.mainrelease/',
                     os.environ['SND2KROOT']+'/',
                     ]

            files = [ ('.'+prefix+'dbrc', 'db'),
                      ('.'+prefix+'rc',   ''),
                    ]

            for d in dirs:
                for (lname, prefix2) in files:
                    testname = d+lname
                    if os.access( testname, os.R_OK):
                        name = testname
                        prefix += prefix2
                        break
                if name: break

            if name==None:
                names = ', '.join(name for (name, _) in files)
                raise EnvironmentError(names+" not found in any standard place")
        else:
            if not os.access(name, os.R_OK):
                raise EnvironmentError("file '%s' is not available"%name)

        if debug: sys.stderr.write('%s: Opening configuration file %s\n'%(prefix, name))

        argprefix = prefix+'-'
        argkeys   = [ argprefix+k for k in self.keys() ]

        reinfo    = re.compile(r'^\s*('+prefix+r'[^= \t\v\n\r]+)\s*=\s*(\S+)\s*$')

        f = open(name, 'r')
        try:
            for line in f:
                if recomment.match(line): continue
                m = reinfo.match(line)
                if not m:
                    raise EnvironmentError('wrong line: '+line)
                if not m.group(1) in argkeys:
                    raise EnvironmentError("wrong key in line: '%s', group is '%s' in %s"%(line.strip(), m.group(1),argkeys,))
                k = m.group(1)
                ptest, pkey = k.split('-')
                if pkey in ('port',):
                    self[pkey] = int(m.group(2))
                else:
                    self[pkey] = m.group(2).strip("\'\"")
        finally:
            f.close()
        assert self['hostname']!=None
        assert self['username']!=None
        assert self['password']!=None
        assert self['dbname']  !=None

    def __getitem__(self, name):
        if name=='rw': return dict.__getitem__(self,'rw')

        if self['rw']:
            name1 = name+'1'
            if name1 in self and dict.__getitem__(self,name1)!=None:
                return dict.__getitem__(self, name1)
        return dict.__getitem__(self, name)

    def __getattr__(self, name):
        return self[name]

if __name__ == "__main__" :
    cro = config(sys.argv[1])
    print('ro: %s:%s@%s:%d/%s'%(cro.hostname, cro.username, cro.password, cro.port, cro.dbname))
    crw = config(sys.argv[1], rw=True)
    print('rw: %s:%s@%s:%d/%s'%(crw.hostname, crw.username, crw.password, crw.port, crw.dbname))
