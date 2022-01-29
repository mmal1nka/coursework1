from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import Person, UserAndMessage
from django.db.utils import IntegrityError
from django.contrib import messages
from .forms import CipherForm


def RegistrationTemplate(request):
    return render(request, 'Vigenere/registration.html')


def Registration(request):
    try:
        if request.method == 'POST':
            user = Person()
            checkLogin = request.POST.get('username')
            checkPassword = request.POST.get('pass')
            if len(checkLogin) > 7 and len(checkPassword) > 7:
                user.Login = request.POST.get('username')
                user.Password = request.POST.get('pass')
                user.save()
                return HttpResponseRedirect('encrypt')
            else:
                messages.error(request, 'Login and password must be over 7 letters')
                return redirect('/')
    except IntegrityError:
        messages.error(request, 'User with this login is already exist')
        return redirect('/')


def EncryptedTemplate(request):
    form = CipherForm()
    data = {
        'form': form
    }
    return render(request, 'Vigenere/encrypter.html', data)


def AuthEncMes(request):
    form = CipherForm(request.POST, request.FILES or None)
    if request.method == "POST":
        username = request.POST.get("Log")
        password = request.POST.get("pass")
        mes = request.POST.get('mes')
        key = request.POST.get('key')
        try:
            checkUserLogin = Person.objects.get(Login=username, Password=password)
            rb = request.POST.get("RB", None)
            if rb in ["Decrypt", "Encrypt"]:
                if rb == "Encrypt":
                    try:
                        ChosenFile = request.FILES['chosenFile']
                        chosenFile = ChosenFile.name
                        path = os.path.abspath(chosenFile)
                        chsFile = open(path, 'a')
                        myfile = File(chsFile)
                        if checkUserLogin is not None:
                            msg = mes
                            key = key
                            EncMes = encrypt(msg, key)
                            if EncMes == '':
                                data = {
                                    'username': username,
                                    'password': password,
                                    'mes': mes,
                                    'key': key,
                                    'result': EncMes
                                }
                                messages.error(request, 'Incorrect message or key')
                                return render(request, "Vigenere/encrypter.html", data)
                            else:
                                data = {
                                    'username': username,
                                    'password': password,
                                    'mes': mes,
                                    'key': key,
                                    'result': EncMes
                                }
                                tmp = UserAndMessage.objects.create(EncryptMessage=EncMes, UserId=checkUserLogin.id)
                                myfile.write("\nYour encrypted message: " + EncMes)
                                myfile.closed
                                return render(request, "Vigenere/encrypter.html", data)
                    except MultiValueDictKeyError:
                        data = {
                            'username': username,
                            'password': password,
                            'mes': mes,
                            'key': key,
                        }
                        messages.error(request, 'You have not chosen file')
                        return render(request, "Vigenere/encrypter.html", data)
                elif rb == "Decrypt":
                    if checkUserLogin is not None:
                        msg = mes
                        key = key
                    try:
                        tmp = UserAndMessage.objects.filter(EncryptMessage=msg, UserId=checkUserLogin.id)
                        if tmp is not None:
                            EncMes = decrypt(msg, key)
                            data = {
                                'username': username,
                                'password': password,
                                'mes': mes,
                                'key': key,
                                'result': EncMes
                            }
                            return render(request, "Vigenere/encrypter.html", data)
                    except UserAndMessage.DoesNotExist:
                        data = {
                            'username': username,
                            'password': password,
                            'mes': mes,
                            'key': key,
                        }
                        messages.error(request, "Message is not found")
                        return render(request, "Vigenere/encrypter.html", data)
        except Person.DoesNotExist:
            messages.error(request, "Wrong login or password")
            return HttpResponseRedirect('encrypt')
    return HttpResponseRedirect('encrypt')


def msg_and_key(msg, key):
    if msg == '' or key == '' or len(msg) < len(key):
        key_map = 'Error'
        return key_map
    else:
        key_map = ""
        j = 0
        for i in range(len(msg)):
            if 65 <= ord(msg[i]) <= 90:
                if j < len(key):
                    key_map += key[j].upper()
                    j += 1
                else:
                    j = 0
                    key_map += key[j].upper()
                    j += 1
            elif 97 <= ord(msg[i]) <= 122:
                if j < len(key):
                    key_map += key[j]
                    j += 1
                else:
                    j = 0
                    key_map += key[j]
                    j += 1
            else:
                key_map += " "
        return key_map


def create_vigenere_table():
    table = []
    for i in range(26):
        table.append([])
    for row in range(26):
        for column in range(26):
            if (row + 65) + column > 90:
                table[row].append(chr((row + 65) + column - 26))
            else:
                table[row].append(chr((row + 65) + column))
    return table


def create_vigenere_table_1():
    table = []
    for i in range(26):
        table.append([])
    for row in range(26):
        for column in range(26):
            if (row + 97) + column > 122:
                table[row].append(chr((row + 97) + column - 26))
            else:
                table[row].append(chr((row + 97) + column))
    return table



def cipher_encryption(message, mapped_key):
    table = create_vigenere_table()
    table1 = create_vigenere_table_1()
    encrypted_text = ""
    if mapped_key == 'Error':
        return encrypted_text
    for i in range(len(message)):
        if 122 >= ord(message[i]) >= 97:
            row = ord(message[i]) - 97
            column = ord(mapped_key[i]) - 97
            encrypted_text += table1[row][column]
        elif 65 <= ord(message[i]) <= 90:
            row = ord(message[i]) - 65
            column = ord(mapped_key[i]) - 65
            encrypted_text += table[row][column]
        else:
            encrypted_text += message[i]
    return encrypted_text
