
from carrefour import carrefour_frutas, carrefour_verduras
from eroski import eroski_frutas, eroski_verduras
from datetime import date
from nlp import preprocessDataPipelineEroski, preprocessDataPipelineCarrefour

if __name__ == "__main__":

    verduras_eroski = eroski_verduras()
    frutas_eroski = eroski_frutas()
    verduras_carrefour = carrefour_verduras()
    frutas_carrefour = carrefour_frutas()

    #
    # # Procesamos los datos NLP
    # verduras_eroski_processed = preprocessDataPipelineEroski(verduras_eroski)
    # frutas_eroski_processed = preprocessDataPipelineEroski(frutas_eroski)
    # verduras_carrefour_processed = preprocessDataPipelineCarrefour(verduras_carrefour)
    # frutas_carrefour_processed = preprocessDataPipelineCarrefour(frutas_carrefour)

    today = date.today()

    verduras_eroski.to_excel("output/verduras_eroski_"+str(today)+".xlsx", index=False)
    frutas_eroski.to_excel("output/frutas_eroski_"+str(today)+".xlsx", index=False)
    verduras_carrefour.to_excel("output/verduras_carrefour_"+str(today)+".xlsx", index=False)
    frutas_carrefour.to_excel("output/frutas_carrefour_"+str(today)+".xlsx", index=False)

    #
    # verduras_eroski_processed.to_excel("output/verduras_eroski_"+str(today)+".xlsx", index=False)
    # frutas_eroski_processed.to_excel("output/frutas_eroski_"+str(today)+".xlsx", index=False)
    # verduras_carrefour_processed.to_excel("output/verduras_carrefour_"+str(today)+".xlsx", index=False)
    # frutas_carrefour_processed.to_excel("output/frutas_carrefour_"+str(today)+".xlsx", index=False)


