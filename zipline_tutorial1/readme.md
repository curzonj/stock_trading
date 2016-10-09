# Notes

I'm following this tutorial: http://www.zipline.io/beginner-tutorial.html

## Conda

- [x] I need to remember how to install and use conda properly. I think I didn't reinstall it when I got my new computer.
- [x] figure out how to use conda: http://conda.pydata.org/docs/test-drive.html

Conda is installed at `~/anaconda` and is in your `PATH` already.

## side note on learning python for the 1st time

Laungages I have played with recently:

* ruby - work
* golang - work
* javascript - space game, eve data warehouse, screeps
* python - data science

## jupyter

I did the basic zipline example to buy 10 shares every day, now I need to visualize the results so I need to install jupyter again.

- [x]  Get jupyter ipython running with conda and create a notebook: https://jupyter.readthedocs.io/en/latest/install.html

I couldn't just use the jupyter install that came with conda by default because I had to create a clean environment to support python 3.4 which zipline requires. All I had to do was:

```bash
conda install jupyter
```

jupyter appears to support file management, terminal support, and generic syntax highlighted text editor in addition to notbooks. That means it's super easy to run notebooks on remote heavy duty servers.

Use the following to run jupyter:

```bash
jupyter notebook
```

## More advanced testing

I'm trying to finish the end of the zipline getting started tutorial, but it keeps giving me different errors.

- [ ] Successfully run the zipline DMA example strategy

```bash
zipline run -f dma_tutorial.py --start 2005-1-1 --end 2014-1-1 -o dma.pickle
```

2 open issues against zipline for my current problems:

* https://github.com/quantopian/zipline/issues/1482
* https://github.com/quantopian/zipline/issues/1469
