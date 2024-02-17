@echo off
setlocal
call E:\miniconda3\Scripts\activate.bat E:\miniconda3
call conda activate cqgui
call conda install -c cadquery -c conda-forge cq-editor=master cairosvg
endlocal