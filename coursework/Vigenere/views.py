from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import Person, UserAndMessage
from django.db.utils import IntegrityError
from django.contrib import messages
from .forms import ShiphrForm


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
    form = ShiphrForm()
    data = {
        'form': form
    }
    return render(request, 'Vigenere/encrypter.html', data)


def AuthEncMes(request):
    form = ShiphrForm(request.POST)
    if request.method == "POST" and form.is_valid():
        username = request.POST.get("Log")
        password = request.POST.get("pass")
        try:
            checkUserLogin = Person.objects.get(Login=username, Password=password)
            if checkUserLogin is not None:
                msg = form.cleaned_data['Mess']
                key = form.cleaned_data['Key']
                mapped_key = msg_and_key(msg, key)
                EncMes = cipher_encryption(msg, mapped_key)
                crt = UserAndMessage.objects.create(EncryptMessage=EncMes, Mess=msg, UserId=checkUserLogin.id)
                messages.success(request, "Your encrypted message: " + EncMes)
                return HttpResponseRedirect('encrypt')
        except Person.DoesNotExist:
            messages.error(request, "Wrong login or password")
            return HttpResponseRedirect('encrypt')
    return HttpResponseRedirect('encrypt')


def msg_and_key(msg, key):
    if msg == '' or key == '':
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
