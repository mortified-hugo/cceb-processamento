from glob import glob

filenames = glob('input/*.xlsx')
analistas = [file.strip('.xlsx').strip('input\\') for file in filenames]

print(analistas)