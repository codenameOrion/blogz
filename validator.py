
def validator(username, password, email, verify):
    
    
    
    #welcome_page = render_template('welcome.html', username=username)
    is_error = False
    

    
    error_user = ''
    error_pass = ''
    error_pass_val = ''
    error_email = ''      
    
    if len(username) < 3 or len(username) > 20 or ' ' in username:
        error_user = "That's not a valid username"
        is_error = True
    if len(password) < 3 or len(password) > 20 or ' ' in username:
        error_pass = "That's not a valid password"
        is_error = True
    if verify != password:
        error_pass_val = "Password does not match"
        is_error = True
    #elif email == '':
        #return welcome_page
    if email != '' and ('@' not in email or len(email) < 3 or len(email) > 20 or ' ' in email):
        error_email = "Not a valid email"
        is_error = True
    
    
    #if is_error == False:
        #return render_template('form.html', error_user=error_user, error_pass=error_pass, error_pass_val=error_pass_val)
    return is_error, error_user, error_pass, error_pass_val, error_email
    
       



