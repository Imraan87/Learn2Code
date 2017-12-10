classdef PythonHandler < handle
    
    
    properties
        VirtEvnPath
        UserBasePath
        UserPaths
        BasePaths
    end
    
    methods
        function Obj = PythonHandler()
            
            Obj.VirtEvnPath  = py.str('C:\Users\Imraan\Desktop\Learn2Code\Python\VirtEnv27_64\Lib\site-packages');
            Obj.UserBasePath = 'C:\Users\Imraan\Desktop\Learn2Code\Matlab\Call PythonLibraries\Test1';
            Obj.generateUserPaths();
            
            Obj.loadPython()
            Obj.setPaths()
            
%             P  = py.sys.path;
%             CP = cell(P);
%             cellfun(@char, CP,'UniformOutput',false)'
            
        end
        
        function loadPython(Obj)
            
            % [version, executable, isloaded] = pyversion(PythonPath);
            [version, executable, isloaded] = pyversion;
            if ~isloaded && ~strcmp(version,'2.7')
                pyversion 2.7
            end
            
            
            switch version
                case '2.7'
                    Obj.getBasePathsV27(executable);
                case '3.5'
                    Obj.getBasePathsV35(executable);
            end
        end
        function generateUserPaths(Obj)
            
            Obj.UserPaths = py.list({Obj.UserBasePath});
        end
        function getBasePathsV27(Obj,PythonPath)
            
            PythonPath = strrep(PythonPath,'\pythonw.exe','');
            Paths      = {'',...
                'C:\WINDOWS\system32\python27.zip',...
                fullfile(PythonPath,'DLLs'),...
                fullfile(PythonPath,'lib'),...
                fullfile(PythonPath,'lib\plat-win'),...
                fullfile(PythonPath,'lib\lib-tk'),...
                fullfile(matlabroot,'bin','win64'),...
                PythonPath,...
                fullfile(PythonPath,'lib\site-packages')};
            
            Obj.BasePaths = py.list(Paths);
            
        end
        function getBasePathsV35(Obj,PythonPath)
            
            PythonPath    = strrep(PythonPath,'\pythonw.exe','');
            Paths         = {'',...
                fullfile(PythonPath,'python35.zip'),...
                fullfile(PythonPath,'DLLs'),...
                fullfile(PythonPath,'lib'),...
                PythonPath,...
                fullfile(PythonPath,'lib\site-packages')};
            
            Obj.BasePaths = py.list(Paths);
        end
        
        function setPaths(Obj)
            
            P  = py.sys.path;
            
            for i = 1:size(P,2)
                while size(P,2) >0
                    P.remove(P{i})
                end
            end
            
            
            for i = 0:size(Obj.BasePaths,2)-1
                insert(py.sys.path,int32(i),Obj.BasePaths{i+1});
            end
            
            N = uint32(cumsum([size(P,2)+1 , 1:size(Obj.UserPaths,2)]));
            insert(py.sys.path, N(1), Obj.VirtEvnPath)
            
            for i = 2:numel(N)
                insert(py.sys.path, N(i), Obj.UserPaths{i-1})
            end
            
        end
    end
    
end

