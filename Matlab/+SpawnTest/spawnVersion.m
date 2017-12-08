function ExitCode = spawnVersion(n)
dbstop in SpawnTest.spawnVersion at 14 if n>=4
%runtime = java.lang.Runtime.getRuntime();
%process = runtime.exec('program arg1 arg2');  % non-blocking
% process = runtime.exec('matlab –r Test1');  % non-blocking
% rc = process.waitFor();    % block Matlab until external program ends
% rc = process.exitValue();  % fetch an ended process' return code
% 
% process.destroy();         % force-kill the process (rc will be 1)
% 

% system('program arg1 arg2'); 

ExitCode = 12;
end

