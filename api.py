import web
import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np
from flask import Flask, render_template



urls = ('/upload', 'Upload')

class Upload ():
    def GET(self):
        web.header("Content-Type","text/html; charset=utf-8")
        return """<html>
        <html><head><meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
	<title>What stung me?</title>
	<!-- CSS only -->
	<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
     crossorigin="anonymous"></head><body><div class="container bg-light ">
     <center>
		<div class="row justify-content-center mt-4 pt-4">
			<div class="col-md-10 ">
            <a href="https://ibb.co/27Dn5xh"><img src="https://i.ibb.co/27Dn5xh/logo.png" alt="logo" border="0" ></a>
            <br>
            <br>
            <br>
             <label class="h1">What stung me?</label> <br>
             <br><br>
                 <form method="POST" enctype="multipart/form-data" action="">
                 <input type="file" name="myfile" />
                <br/><br/>
                <button  class="btn btn-secondary input type="submit"> Subir </button> <br> <br> 
                  </form>
        </center>
        </body>
        </div></<div>
        </html>



</html>"""

    def POST(self):
        x = web.input(myfile={})
        filedir = '/workspace/quemepicodemo41/quemepico/static' # change this to the directory you want to store the file in.
        if 'myfile' in x: # to check if the file-object is created
            filepath=x.myfile.filename.replace('\\','/') # replaces the windows-style slashes with linux ones.
            filename=filepath.split('/')[-1] # splits the and chooses the last part (the filename with extension)
            fout = open(filedir +'/'+ filename,'wb') # creates the file where the uploaded file should be stored
            fout.write(x.myfile.file.read()) # writes the uploaded file to the newly created file.
            fout.close() # closes the file, upload complete.
     
        np.set_printoptions(suppress=True)
        # Disable scientific notation for clarity


            # Load the model
        model = tensorflow.keras.models.load_model('/workspace/quemepicodemo41/quemepico/static/keras_model.h5')
# Create the array of the right shape to feed into the keras model
# The 'length' or number of images you can put into the array is
# determined by the first position in the shape tuple, in this case 1.
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

# Replace this with the path to your image
        image = Image.open('/workspace/quemepicodemo41/quemepico/static/'+filename)

#resize the image to a 224x224 with the same strategy as in TM2:
#resizing the image to be at least 224x224 and then cropping from the center
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.ANTIALIAS)

#turn the image into a numpy array
        image_array = np.asarray(image)

# display the resized image
        image.show()

        # Normalize the image
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
        # Load the image into the array
        data[0] = normalized_image_array

# run the inference
        prediction = model.predict(data)
        for i in prediction: 
                if i[0] > 0.85:
                    titulo = " Te pico una abeja\nEl dolor es muy intenso asi que tienes que tener cuidado. ¡OJO SI ERES ALERGICO ACUDE RAPIDDO A UN MEDICO!\nLavar la zona afectada con agua y con jabon. Enfriar la picadura con hielo. Aplicar un antiséptico. Nunca se debe de apretar la picadura de abeja o avispa para tratar de sacar el veneno, ya que este puede extenderse. Se puede paliar el dolor y las molestias con una crema para el picor y un antihistamínico"
                    

                elif i[1] > 0.85:
                    titulo = "Te pico un mosquito\nNo te preocupes, una picadura de mosco no es grave. ¡OJO SI ERES ALERGICO ACUDE RAPIDDO A UN MEDICO!\nAplica loción, crema o pasta. Aplicar una loción de calamina o una crema de hidrocortisona de venta libre en la picadura puede ayudar a aliviar la picazón. O bien, prueba a untar la picadura con una pasta preparada con bicarbonato de sodio y agua. Vuelve a aplicarla varias veces al día hasta que los síntomas desaparezcan."
                    

                elif i[2] > 0.85:
                    titulo = "Te pico una chinche\nNo tienes de que preocuparte no es nada grave. ¡OJO SI ERES ALERGICO ACUDE RAPIDDO A UN MEDICO!\nSi crees que te ha picado una chinche, lava la picadura con agua y jabón y ponte loción de calamina para aliviar el picor. Un adulto puede conseguir una crema para aliviar la picazón en una farmacia o droguería. Intenta rascar la picadura lo menos posible porque se te podría infectar."
                   

                elif i[3] > 0.85:
                    titulo = "Te pico una garrapata\nSi te pico una garrapata tienes que tener cuidado, porque pueden trasmitirte enfermedades graves\nUtiliza pinzas pequeñas o de punta fina para agarrar la garrapata lo más cerca posible de la piel. Saca suavemente la garrapata con un movimiento ascendente lento y constante. No la retuerzas ni la aprietes. No agarres la garrapata con las manos desprotegidas. Los expertos no recomiendan usar vaselina, esmalte de uñas ni cerillas (fósforos) calientes para quitar garrapatas."
                   

                elif i[4] > 0.85:
                    titulo = "Te pico una Hormiga\nNo tienes de que preocuparte no es grave solo tendras un leve hinchazón ¡OJO SI ERES ALERGICO ACUDE RAPIDO A UN MEDICO!\nSi alguna vez crees que te ha picado una hormiga.  El veneno de las picaduras de hormigas coloradas puede producir una ligera hinchazón en la zona de la picadura, y puede que el médico quiera echarle un vistazo para asegurarse de que no tienes una reacción alérgica."
                   

                elif i[5] > 0.85:
                    titulo = "Te pico una Pulga\nNo tienes de que preocuparte no es grave solo tendras un leve hinchazón ¡OJO SI ERES ALERGICO ACUDE RAPIDO A UN MEDICO!\nSi crees que te ha picado una pulga, lava la picadura con agua y jabón. Aplica loción de calamina para aliviar la picazón, o un adulto puede conseguirse en la farmacia una crema que alivie la picazón. Trata de no rascarte demasiado porque las picaduras podrían infectarse."
                    
                elif i[6] > 0.85:
                    titulo = "Te pico una Araña\n Puedes presentar dolor muy severo ¡OJO SI ERES ALERGICO ACUDE RAPIDO A UN MEDICO!\nLave el área afectada con agua y jabón. Aplique hielo o una compresa húmeda. Si necesita, tome un medicamento para el dolor de venta libre. Considere tomar remedios para la alergia en caso de hinchazón severa. Busque tratamiento médico para niños y adultos con síntomas graves. Lave el área afectada con agua y jabón  Aplique hielo o una compresa húmeda.Si necesita, tome un medicamento para el dolor de venta libre. Considere tomar remedios para la alergia en caso de hinchazón severa Busque tratamiento médico para niños y adultos con síntomas graves"
                   
                else:  
                    titulo = "Hay un error\nLa imagen que nos eviaste no la reconosemos, puedes intentar con otra imagen "
                    
        return titulo
        raise web.seeother('/upload')

if __name__ == "__main__":
   app = web.application(urls, globals()) 
   app.run()