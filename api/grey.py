 <div class="containers">
               <div >
  
                <form  id="upload_form" method="post" action="/product_list"   enctype="multipart/form-data" >  
                   
                        <div class="form-rows" >
                         
                       
                        <div class="title-left"  >
                            <strong></strong><output id="list" style="overflow-y:auto; height: 300px; overflow-x:hidden; display: inline-block; font-size: 20px; color: red;"></output></strong>
                       

                         <center> <div class="file-upload">
                                <div class="file-select">
                                    <label for="files" class="mb-0"><strong> <li class="fa fa-upload"> &nbsp;&nbsp;Add Image  </li></strong></label></center>
                                    <div class="file-select-button" id="fileName" hidden="true">Choose Image</div>
                                    <div class="file-select-name" id="noFile" hidden="true"></div>
                                    <input type="file" id="files" name="files[]"  hidden="true" required="true"  multiple />
                                </div>
                            </div>
                             </div>
                        </div>

                      </center>
                        <script type="text/javascript">
                          
                         function deleteImage() { 
                              var index = Array.from(document.getElementById('list').children).indexOf(event.target.parentNode)
                                document.querySelector("#list").removeChild( document.querySelectorAll('#list span')[index]);
                                totalFiles.splice(index, 1);
                                console.log(totalFiles)
                            }

                            var totalFiles = [];
                            function handleFileSelect(evt) {
                                var files = evt.target.files; // FileList object

                                // Loop through the FileList and render image files as thumbnails.
                                for (var i = 0, f; f = files[i]; i++) {

                                  // Only process image files.
                                  if (!f.type.match('image.*')) {
                                    continue;
                                  }
                                  
                                  totalFiles.push(f)

                                  var reader = new FileReader();

                                  // Closure to capture the file information.
                                  reader.onload = (function(theFile) {
                                    return function(e) {
                                      // Render thumbnail.
                                      var span = document.createElement('span');
                                      span.innerHTML = ['<img width=400 class="d-block w-100" src="', e.target.result,
                                                        '" title="', escape(theFile.name), '"/>', "<li class='fa fa-trash'  onclick='deleteImage()'>&nbsp;&nbsp;</li>"].join('');

                                      document.getElementById('list').insertBefore(span, null);
                                    };
                                  })(f);

                                  // Read in the image file as a data URL.
                                  reader.readAsDataURL(f);
                                }
                              }
                              

                              document.getElementById('files').addEventListener('change', handleFileSelect, false);

                        </script>


                       
                        
 
   <center>
  <b>

                               <label for="product_name"> Product name *</label><br>
                               
                                    <input id="product_name" name= "product_title" id="product_title" type="text"><br>
                           
                            
                                <label for="product_category">  Product category *</label><br>
                               
                                     <input name="product_category" id="product_category"  type="text"><br>
                              
                            

                            
                                <label for="price"> Price *</label><br>
                                 <input name="price" id="price"  type="text"><br>
                                
                           

                         
                                <label for="product_decsription">Product decsription *</label><br>
                               <textarea name="product_description" id="product_decsription"></textarea><br>
                               <li><input class="mb-0" id="latlng" name="latlng" hidden="true"></input></li></div>
                                                            
                          
    
     
    
  </b>
  </center>
   
    <button type="submit" class="btn hvr-hover"><li class="fa fa-send"> Submit </li></button>
    </form>

   </div>

























    <div class="containers">
              
  
               <form id="formAjax" action="/product_list" method="post" enctype="multipart/form-data">
                   
                        <div class="form-rows" >
                         
                       
                        <div class="title-left"  >
                            <strong></strong><output id="list" style="overflow-y:auto; height: 300px; overflow-x:hidden; display: inline-block; font-size: 20px; color: red;"></output></strong>
                       

                         <center> 
                          

                          <div class="file-upload">
                                <div class="file-select">
                                    <label for="files" class="mb-0"><strong> <li class="fa fa-upload"> &nbsp;&nbsp;Add Image  </li></strong></label></center>
                                    <div class="file-select-button" id="fileName" hidden="true">Choose Image</div>
                                    <div class="file-select-name" id="noFile" hidden="true"></div>
                                    <input type="file" id="files" name="files[]"  hidden="true" required="true"  multiple />
                                </div>
                            </div>
                             </div>

                        
                   
                                                     <label for="product_name"> Product name *</label><br>
                                                     
                                                          <input id="product_name" name= "product_title" id="product_title" type="text"><br>
                                                 
                                                  
                                                      <label for="product_category">  Product category *</label><br>
                                                     
                                                           <input name="product_category" id="product_category"  type="text"><br>
                                                    
                                                  

                                                  
                                                      <label for="price"> Price *</label><br>
                                                       <input name="price" id="price"  type="text"><br>
                                                      
                                                 

                                               
                                                      <label for="product_decsription">Product decsription *</label><br>
                                                     <textarea name="product_description" id="product_decsription"></textarea><br>
                                                     <li><input class="mb-0" id="latlng" name="latlng" hidden="true"></input></li></div>
                                                                                  
                                                
                          
                           
                          
                        </b>
                        </center>

                          <button  id="submit" type="submit" class="btn hvr-hover"  onclick="postimage()"><li class="fa fa-send"> Submit </li></button>
                    </form>


                        </div>

                        <script type="text/javascript">


                            function postimage(){
                                      let formData = new FormData();
                                      let ins = document.getElementById('files').files.length;
                                      for (var x = 0; x < ins; x++) {
                                      form_data.append("files[]", document.getElementById('files').files[x]);
                                      }    
                                      console.log('Sending...');

                                    }
                                

    

                          
                         function deleteImage() { 
                              var index = Array.from(document.getElementById('list').children).indexOf(event.target.parentNode)
                                document.querySelector("#list").removeChild( document.querySelectorAll('#list span')[index]);
                                totalFiles.splice(index, 1);
                                console.log(totalFiles)
                            }

                        

                            

                            var totalFiles = [];
                            function handleFileSelect(evt) {
                                var files = evt.target.files; // FileList object

                                // Loop through the FileList and render image files as thumbnails.
                                for (var i = 0, f; f = files[i]; i++) {

                                  // Only process image files.
                                  if (!f.type.match('image.*')) {
                                    continue;
                                  }
                                  
                                  totalFiles.push(f)

                                  var reader = new FileReader();

                                  // Closure to capture the file information.
                                  reader.onload = (function(theFile) {
                                    return function(e) {
                                      // Render thumbnail.
                                      var span = document.createElement('span');
                                      span.innerHTML = ['<img width=400 class="d-block w-100" src="', e.target.result,
                                                        '" title="', escape(theFile.name), '"/>', "<li class='fa fa-trash'  onclick='deleteImage()'>&nbsp;&nbsp;</li>"].join('');

                                      document.getElementById('list').insertBefore(span, null);
                                    };
                                  })(f);

                                  // Read in the image file as a data URL.
                                  reader.readAsDataURL(f);
                                }
                              }
                              

                              document.getElementById('files').addEventListener('change', handleFileSelect, false);

                        </script>


          </div>
        </div>
      
                        
      

   
   </div>
                


        </div>




















        if request.method == 'POST':
          
        #get  userdata
        username =session["current_user"]
        user_data =Users.query.filter_by(username= username).first()    
        
        data= request.form
        author_id = business_data.id
        product_title= data.get('product_name')
        product_description = data.get('product_description')
        product_category = data.get('product_category')
        price = data.get('product_cost')
        status = 0
        timestamp =sasa

        product_data = db.session.query(Products).filter(and_(Products.product_title == product_title, Products.price ==price, Products.status ==0, Products.author_id ==author_id)).first()
        if product_data:
          flash(" Product exists in active state, No need to repost!")
          return render_template("dashboard.html", user_data=user_data)

          
         
        new_product = Products(
            product_title = product_title,
            product_description = product_description,
            author_id = author_id,            
            product_category = product_category,
            price = price,
            status = 0,
            timestamp = sasa
            )

        db.session.add(new_product)
        db.session.commit()

      
        product_data = db.session.query(Products).filter(and_(Products.product_title == product_title, Products.price ==price)).first()
        username =session["current_user"]
        user_data =Users.query.filter_by(username= username).first()
        business_data = Business.query.filter_by(owner = user_data.username).first()


