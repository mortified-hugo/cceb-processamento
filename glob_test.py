from glob import glob

filenames = glob('input/new/*.xlsx')
analistas = [file.strip('.xlsx').strip('input/new\\') for file in filenames]

print(analistas)