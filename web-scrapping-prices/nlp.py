# Data processing pipeline

import pandas as pd

# verduras_eroski = pd.read_excel("output/verduras_eroski_2022-03-29.xlsx")
# frutas_eroski = pd.read_excel("output/frutas_eroski_2022-03-29.xlsx")
# verduras_carrefour = pd.read_excel("output/verduras_carrefour_2022-04-04.xlsx")
frutas_carrefour = pd.read_excel("output/frutas_carrefour_2022-03-24.xlsx")
# #
# # # Añadimos una columna con categoría
dataset = frutas_carrefour.copy()


def preprocessDataPipelineEroski(dataset):

    print('Preprocess Eroski')

    import re
    import string
    from num2words import num2words
    import spacy
    from spacy.lang.es.examples import sentences

    import nltk
    from nltk.corpus import stopwords
    STOP_WORDS = stopwords.words('spanish')
    STOP_WORDS.append('eroski')
    STOP_WORDS.append('aprox')
    STOP_WORDS.append('label')
    STOP_WORDS.append('malla')
    STOP_WORDS.append('peso')
    STOP_WORDS.append('manojo')
    STOP_WORDS.append('natur')
    STOP_WORDS.append('país')
    STOP_WORDS.append('vasco')
    STOP_WORDS.append('g')
    STOP_WORDS.append('kg')
    STOP_WORDS.append('compra')
    STOP_WORDS.append('mínima')
    STOP_WORDS.append('bolsa')
    STOP_WORDS.append('especial')

    numbers = lambda x: re.sub("[^0-9]", '', x)
    dataset['Peso [gramos]'] = dataset.Producto.map(numbers)
    comas = lambda x: re.sub(",", '.', x)
    dataset['Precio'] = dataset.Precio.map(comas)

    # Transformo a INT los gramos de la compra
    for i in list(range(0, len(dataset))):
        if not dataset['Peso [gramos]'][i]:
            dataset['Peso [gramos]'][i] = 0
        else:
            dataset['Peso [gramos]'][i] = int(dataset['Peso [gramos]'][i])

    # Transformo a FLOAT el precio
    for i in list(range(0, len(dataset))):
        if not dataset['Precio'][i]:
            dataset['Precio'][i] = 0
        else:
            dataset['Precio'][i] = float(dataset['Precio'][i])

    # Pasamos los kilogramos a gramos, y las unidades (0 gramos) a 'unidades'.
    for i in list(range(0, len(dataset))):
        if dataset['Peso [gramos]'][i] < 10:
            dataset['Peso [gramos]'][i] = dataset['Peso [gramos]'][i]*1000

        if (dataset['Peso [gramos]'][i] > 0 and dataset['Peso [gramos]'][i] != 'unidad') and dataset['Peso [gramos]'][i] < 10:
            dataset['Peso [gramos]'][i] = dataset['Peso [gramos]'][i]*1000


    alphanumeric = lambda x: re.sub('\w*\d\w*', ' ', x)
    punc_lower = lambda x: re.sub('[%s]' % re.escape(string.punctuation), ' ', x.lower().strip())
    new_line = lambda x: re.sub('\n', ' ', x)
    stopw = lambda x: ' '.join([word for word in x.split() if word not in (STOP_WORDS)])

    from datetime import date

    dataset['textoProcesado'] = dataset.Producto.map(alphanumeric).map(punc_lower).map(new_line).map(stopw)

    for i in list(range(0, len(dataset))):
        if dataset['Peso [gramos]'][i] == 0:
            dataset['Peso [gramos]'][i] = 'unidad'

    dataset['Categoria'] = dataset['textoProcesado'].str.split().str.get(0)
    dataset['SubCategoria'] = dataset['textoProcesado'].str.split().str.get(1)
    dataset['Fecha'] = date.today()
    dataset['Supermercado'] = 'Eroski'

    # Elimino columnas innecesarias
    dataset.drop('textoProcesado', inplace=True, axis=1)
    dataset = dataset.reindex(columns=['Supermercado', 'Fecha', 'Categoria', 'SubCategoria', 'Precio', 'Peso [gramos]'])

    return dataset


def preprocessDataPipelineCarrefour(dataset):

    print('Carrefour')

    import re
    import string
    import nltk
    from nltk.corpus import stopwords
    STOP_WORDS = stopwords.words('spanish')
    STOP_WORDS.append('Carrefour')
    STOP_WORDS.append('aprox')
    STOP_WORDS.append('label')
    STOP_WORDS.append('malla')
    STOP_WORDS.append('peso')
    STOP_WORDS.append('manojo')
    STOP_WORDS.append('g')
    STOP_WORDS.append('kg')
    STOP_WORDS.append('compra')
    STOP_WORDS.append('mínima')
    STOP_WORDS.append('bolsa')
    STOP_WORDS.append('especial')
    STOP_WORDS.append('100%')
    STOP_WORDS.append('72h')


    dataset.dropna(subset=['Precio'], inplace=True)
    dataset.reset_index(drop=True, inplace=True)

    comas = lambda x: re.sub(",", '.', x)
    dataset['Precio'] = dataset.Precio.map(comas)


    numbers = lambda x: re.sub("[^0-9]", '', x)
    dataset['Peso [gramos]'] = dataset.Producto.map(numbers)

    # for i in list(range(0, len(dataset))):
    #     if not dataset['Peso [gramos]'][i]:
    #         dataset['Peso [gramos]'][i] = 0
    #     else:
    #         dataset['Peso [gramos]'][i] = int(dataset['Peso [gramos]'][i])

    # # Transformo a INT los gramos de la compra
    import pandas as pd
    dataset['Peso [gramos]'] = pd.to_numeric(dataset['Peso [gramos]'], errors='coerce')


    # Pasamos los kilogramos a gramos, y las unidades (0 gramos) a 'unidades'.
    for i in list(range(0, len(dataset))):
        if dataset['Peso [gramos]'][i] < 6:
            dataset['Peso [gramos]'][i] = dataset['Peso [gramos]'][i]*1000

        elif dataset['Peso [gramos]'][i] == 0:
            dataset['Peso [gramos]'][i] = 500

        else:
            dataset['Peso [gramos]'][i] = 1000


    alphanumeric = lambda x: re.sub('\w*\d\w*', ' ', x)
    punc_lower = lambda x: re.sub('[%s]' % re.escape(string.punctuation), ' ', x.lower().strip())
    new_line = lambda x: re.sub('\n', ' ', x)
    stopw = lambda x: ' '.join([word for word in x.split() if word not in (STOP_WORDS)])
    remove_specialCharacters = lambda x: re.sub('[\n]', '', x)
    remove_euro = lambda x: re.sub('[€]', '', x)
    remove_euro_kg = lambda x: re.sub('[€/kg]', '', x)
    numbers = lambda x: re.sub('[0-9]+', ' ', x)
    ud = lambda x: re.sub('[ud]+', ' ', x)


    dataset['textoProcesado'] = dataset.Producto.map(alphanumeric).map(punc_lower).map(new_line).map(stopw)
    dataset['Precio'] = dataset.Precio.map(remove_specialCharacters).map(remove_euro_kg).map(remove_euro).map(ud)

    dataset['Precio'] = dataset['Precio'].str.split().str.get(0)


    # Transformo a FLOAT el precio
    for i in list(range(0, len(dataset))):
        if not dataset['Precio'][i]:
            dataset['Precio'][i] = 0
        else:
            dataset['Precio'][i] = float(dataset['Precio'][i])


    from datetime import date

    dataset['Categoria'] = dataset['textoProcesado'].str.split().str.get(0)
    dataset['SubCategoria'] = dataset['textoProcesado'].str.split().str.get(1)
    dataset['Fecha'] = date.today()
    dataset['Supermercado'] = 'Carrefour'

    # Elimino columnas innecesarias
    dataset.drop('textoProcesado', inplace=True, axis=1)
    dataset = dataset.reindex(columns=['Supermercado', 'Fecha', 'Categoria', 'SubCategoria', 'Precio', 'Peso [gramos]'])

    return dataset
# #
finalData = preprocessDataPipelineCarrefour(dataset)
finalData.to_excel("frutas_carrefour_24032022_KC.xlsx", index=False)