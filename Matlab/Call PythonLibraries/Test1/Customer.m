classdef Customer < handle
    %UNTITLED Summary of this class goes here
    %   Detailed explanation goes here
    
    properties(SetAccess = 'private')
        Python = py.people.Customer('N/A',0);
    end
    
    methods
        function Obj = Customer(Name,Balance)
            
            Obj.Python.name    = Name;
            Obj.Python.balance = Balance;
            
        end
    end
    methods
        function B = subsref(A,S) 
           A 
        end
    end
    
end

