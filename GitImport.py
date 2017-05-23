
import requests
from collections import defaultdict

'''
Objective:
The purpose of this file is to make it easy to import python
files and functions that exist in a GitHub repository.
By doing so,imports can be more modular and less dependent
on hard-code files being present and up-to-date.


# URL = BasePath+UserName+RepoName+BranchName+FilePath
A = 'https://raw.githubusercontent.com/jrolf/JStore/master/jstore.py'

BasePath = 'https://raw.githubusercontent.com'
UserName = 'jrolf'
RepoName = 'JStore'
BrchName = 'master'
FilePath = 'jstore.py'

URL = '/'.join([BasePath,UserName,RepoName,BrchName,FilePath]) 

#URL==A

'''

#######################################################################


class GitImport(object):
    def __init__(self,User='',Pass=''):
        self.SaveAuth(User,Pass) 
        self.SetBasePath()
        self.SetBrchName()
        self.rows = [] 
        self.funcs = defaultdict(list)
        
    def SaveAuth(self,User,Pass):
        self.username = User
        self.password = Pass
        
    def SetBasePath(self,BasePath='https://raw.githubusercontent.com'):
        self.basepath = BasePath
        
    def SetBrchName(self,BrchName='master'):
        self.brchname = BrchName
        
    def GenerateURL(self,FullPath='jrolf/JStore/jstore.py'): 
        L = FullPath.split('/') 
        self.repouser = L[0]
        self.reponame = L[1]
        self.filepath = '/'.join(L[2:])  
        L2 = [self.basepath,
              self.repouser,
              self.reponame,
              self.brchname,
              self.filepath]  
        self.URL = '/'.join(L2) 
        
    def PullRows(self,FullPath='jrolf/JStore/jstore.py'):  
        self.GenerateURL(FullPath=FullPath)
        if self.password:
            Auth = (self.username,self.password)
            r = requests.get(self.URL, auth=Auth) 
        else:
            r = requests.get(self.URL)
        rows = list(r.content.split('\n'))
        rows = [a.replace("\\",'') for a in rows] 
        self.rows = rows 
        
    def PrintRows(self): 
        for r in self.rows:
            print r
        
    def Import(self,FullPath='jrolf/JStore/jstore.py'):
        self.PullRows(FullPath)
        L = self.rows
        CodeString = '\n'.join(L)
        return CodeString
    
    def ParseFuncs(self,FullPath='jrolf/JStore/jstore.py'):
        if not self.rows and FullPath:
            self.PullRows(FullPath) 
        fname = '' # Function Name 
        for s in self.rows:
            if not s.strip(): continue 
            if s.startswith('import') or s.startswith('from'):
                self.funcs['imports'].append(s.strip())  
            elif len(s)>3 and s[:3] in ['def','cla']:   
                fname = s.split('(')[0].split()[-1] 
                self.funcs[fname].append(s)
            elif s[0]!=' ':
                fname = '' 
            elif s[0]==' ' and fname:
                self.funcs[fname].append(s)
                
    def GetFuncNames(self):
        return sorted(self.funcs)
    
    def GetFuncRows(self,FuncName):
        return self.funcs[FuncName]
    
    def PrintFunc(self,FuncName):
        for line in self.funcs[FuncName]:
            print line
    
    def GetFuncString(self,FuncName):
        rows = self.funcs[FuncName]   
        CodeString = '\n'.join(rows)
        return CodeString
    
    def GetFuncStrings(self,FuncNameList=[]):
        if not FuncNameList:
            FuncNameList = self.GetFuncNames() 
        D = {}
        for fname in FuncNameList:
            D[fname] = self.GetFuncString(fname) 
        return D
    

#######################################################################

