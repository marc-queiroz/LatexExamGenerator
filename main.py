#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'marc'

from dominio import Exercicio,Questao,EstruturaArquivos
from random import shuffle, randrange
from Crypto import Random
from Crypto.Cipher import AES

import qrcode
from qrcode.image.pil import PilImage

import os
import re
import shutil
import binascii

def pad(s):
    return s + b"\0" * (AES.block_size - len(s) % AES.block_size)


def encrypt(message, key, key_size=256):
    message = pad(message)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(message)


def decrypt(ciphertext, key):
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext[AES.block_size:])
    return plaintext.rstrip(b"\0")


def encrypt_file(file_name, key):
    with open(file_name, 'rb') as fo:
        plaintext = fo.read()
    enc = encrypt(plaintext, key)
    with open(file_name + ".enc", 'wb') as fo:
        fo.write(enc)


def decrypt_file(file_name, key):
    with open(file_name, 'rb') as fo:
        ciphertext = fo.read()
    dec = decrypt(ciphertext, key)
    with open(file_name[:-4], 'wb') as fo:
        fo.write(dec)


def adicionarArquivos(diretorioAtual, resultado):
    for (dirpath, dirnames, filenames) in os.walk(diretorioAtual):
        novoNo = EstruturaArquivos.EstruturaArquivos(dirpath + '/',dirnames,filenames)
        if novoNo not in resultado:
            resultado[diretorioAtual] = novoNo
            for novoDir in dirnames:
                if 'question' in (dirpath + '/' + novoDir):
                    print 'Adicionando:' + dirpath +'/'+ novoDir
                    # print '/.' in novoNo.diretorioAtual
                    adicionarArquivos(novoDir, resultado)
        else:
            print 'Diretório já adicionado'
            return

    return resultado

if __name__ == "__main__":
    currentWorkDirectory = os.getcwd()
    print 'Diretório atual: ' + currentWorkDirectory

    """ Testando funcionalidade - Adicionar Arquivos """
    estrutura = dict()
    adicionarArquivos(currentWorkDirectory, estrutura)

    # PARA DEBUGAR OS DIRETORIOS
    # for i in estrutura.viewvalues():
    #     print 'Diretorio:' + i.diretorioAtual
    #     print 'Diretorios contidos:' + str(i.diretorios)
    #     print '/.' in i.diretorioAtual
    # PARA DEBUGAR OS DIRETORIOS

    """ Criando o shuffle nos exercícios
     Se entrar no diretorio de exercícios e o mesmo contiver
     um arquivo SHUFFLE, deverá abrir o arquivo template
     normalmente o arquivo exercise.0 . Então deverá gerar
     arquivos a partir desse. Uma quantidade N de arquivos
     no qual a diferença será a posição da resposta na prova.
     Cada template deverá conter tags que identificam a região
     que deverá passar pelo regex."""

    """ Quantidade arquivos a serem gerados """
    qtdTemplates = 10

    #Localizar apenas o SHUFFLE dentro do diretorio question
    for e in estrutura.viewvalues():
        if 'question' in e.diretorioAtual and 'SHUFFLE' in os.listdir(e.diretorioAtual):
            print 'Encontrou SHUFFLE no dir:' + e.diretorioAtual
            contador = 0
            for arquivo in e.arquivos:
                if 'exercise' in str(arquivo) and not '~' in str(arquivo):
                    print arquivo
                    contador = contador + 1

            print 'Quantidade de arquivos: ' + str(contador)

            for arquivo in e.arquivos:
                if 'exercise' in str(arquivo) and not '~' in str(arquivo):
                    print e.diretorioAtual + arquivo
                    with open(e.diretorioAtual+arquivo,'r') as fileOpened:
                        ch = fileOpened.read()
                    fileOpened.close()
                    #print file.readlines()
                    regex = re.compile(r'begin(.*)end', re.DOTALL)
                    match = regex.findall(ch)
                    if match:
                        # print match[0]
                        regex = re.compile((r'(\\item.*)'))
                        items = regex.findall(match[0])
                        if items:
                            for i in range(qtdTemplates):
                                novaLista = items[:]
                                shuffle(novaLista)
                                # gerando o gabarito para provas objetivas
                                for idx, item in enumerate(novaLista):
                                    if '%verdadeiro' in item:
                                        print idx
                                        print item
                                novoArquivo = open(e.diretorioAtual+'exercise.'+str(i+1)+'.tex', 'w')
                                regex = re.compile(r'(.*\\begin\{choices\}\n)', re.DOTALL)
                                match = regex.findall(ch)
                                for linha in match:
                                    novoArquivo.write(linha)
                                for linha in novaLista:
                                    novoArquivo.write(linha+'\n')
                                regex = re.compile(r'(\\end\{choices\}\n.*)', re.DOTALL)
                                match = regex.findall(ch)
                                for linha in match:
                                    novoArquivo.write(linha+'\n')
                                novoArquivo.close()

    """ Segunda parte do projeto, gerar os arquivos tex
    em conjunto com os arquivos de gabarito. """

    key = b'\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18'

    #encrypt_file('to_enc.txt', key)
    #decrypt_file('to_enc.txt.enc', key)

    # img = qrcode.make('http://professor.local:8080/ALGUMACOISAAQUIDENTRO/', image_factory=PilImage)
    # img.save('/tmp/output.png')

    arquivoAlunos = open('alunos.txt', 'r')
    relacaoAlunos = arquivoAlunos.readlines()
    arquivoAlunos.close()
    alunos = [line.strip() for line in relacaoAlunos]
    buildDir = 'build'
    diretorioPython = os.path.dirname(os.path.realpath(__file__))
    if buildDir in os.listdir(currentWorkDirectory):
        shutil.rmtree(buildDir)

    if buildDir not in os.listdir(currentWorkDirectory):
        print 'NAO EXISTE O DIRETORIO'
        os.mkdir(buildDir)
        print 'Copiando script.sh para raiz do ' + buildDir + ':'
        shutil.copy(diretorioPython + '/' + 'script.sh', buildDir + '/' + 'script.sh')

    for idxAluno, aluno in enumerate(alunos):
        print aluno

        """ Arquivo de assinatura """
        """ Nome do aluno: """
        """ Ordem da Questão em relação a posição original """

        assinatura = 'Ordem: ' + str(idxAluno) + ', Aluno: ' + aluno + '\n'

        """ Do diretório corrente pegar todas as questões """
        todasQuestoes = []
        profundidade = 0
        for _, diretorios, _ in os.walk(currentWorkDirectory):
            for diretorio in diretorios:
                if 'question' in diretorio:
                    todasQuestoes.append(diretorio)
            profundidade = profundidade + 1
            if (profundidade>0):
                break

        print todasQuestoes

        with open('exam.tex', 'r') as fileOpened:
            ch = fileOpened.read()
        fileOpened.close()


        questoes = todasQuestoes[:]
        shuffle(questoes)

        regex = re.compile(r'\\input\{(question.*)\}')
        match = regex.findall(ch)
        # for result in match:
        #     chBuild = ch[:]
        #     print result
        #     regex = re.compile(result)
        #     match = regex.findall(ch)

        """ Fazendo a relacao entre as questoes originais e as novas
        questões que vão substituir.
        Ex: questao.0/exercise.0 entrada original
        questao.8/exercise.3 saída modificada"""
        novaQuestao = ch[:]
        templateFilenameDirectory = str("%02d" % int(idxAluno+1)) + "_" + re.sub(r'(\s)', r'_', aluno.replace('\n', ''))
        nomeDiretorioAluno = templateFilenameDirectory
        nomeArquivoAluno = nomeDiretorioAluno + '/' + templateFilenameDirectory + ".tex"
        if nomeDiretorioAluno not in os.listdir(buildDir):
            print os.listdir(buildDir)
            print 'Não existe o diretório do aluno: ' + nomeDiretorioAluno
            os.mkdir(buildDir + '/' + nomeDiretorioAluno)

        for idx, questao in enumerate(match):
            print 'idx = ' + str(idx)
            print questoes[idx]
            print 'Arquivos: ' + str((estrutura[questoes[idx]]).exercicios)
            qtdeExercicios = len(estrutura[questoes[idx]].exercicios)
            if qtdeExercicios > 1:
                idxExercise = randrange(1, qtdeExercicios)
                print 'Vai tentar abrir o arquivo: ' + str(estrutura[questoes[idx]].diretorioAtual) + str(estrutura[questoes[idx]].exercicios[idxExercise])
                with open(str(estrutura[questoes[idx]].diretorioAtual) + str(estrutura[questoes[idx]].exercicios[idxExercise]), 'r') as exerciseFile:
                        exerciseContent = exerciseFile.read()
                exerciseFile.close()
                regex = re.compile((r'(\\item.*)'))
                items = regex.findall(exerciseContent)
                # if items:
                #     print 'Itens: ' + items
                for idxAnswer, item in enumerate(items):
                    if '%verdadeiro' in item:
                        assinatura = assinatura + str(idx+1) + ': GABARITO: ' + str(idxAnswer+1) + '\n'
                        assinatura = assinatura + '\tQuestão trocada: ' + questao + '\n'
                        assinatura = assinatura + '\tQuestao escolhida: ' + str(estrutura[questoes[idx]].diretorioAtual) + str(estrutura[questoes[idx]].exercicios[idxExercise]) + '\n'
            else:
                idxExercise = 0
            arquivoOrigemExercicio = str(estrutura[questoes[idx]].diretorioAtual) + str(estrutura[questoes[idx]].exercicios[idxExercise])
            print 'Questao escolhida: ' + arquivoOrigemExercicio
            novoExercicio = str(estrutura[questoes[idx]].diretorioAtual) + str(estrutura[questoes[idx]].exercicios[idxExercise])[:-4]
            print 'Questão a ser substituida: ' + questao
            print 'Nova questão: ' + novoExercicio
            novaQuestao = re.sub(questao, novoExercicio, novaQuestao)
            """ Copiar arquivos escolhidos """
            diretorioDestinoExercicio = buildDir + '/' + nomeDiretorioAluno + '/' + str(estrutura[questoes[idx]].diretorioAtual)[:-1]
            os.mkdir(diretorioDestinoExercicio)
            shutil.copy(arquivoOrigemExercicio, diretorioDestinoExercicio + '/' + str(estrutura[questoes[idx]].exercicios[idxExercise]))
            print "Diretorio de exercicio a ser criado: " + str(estrutura[questoes[idx]].diretorioAtual)[:-1]


        """ Mudar o nome do aluno no arquivo tex """
        novaQuestao = re.sub(r'Nome:\\hfill', 'Nome: ' + str("%02d" % (idxAluno+1)) + ' - ' + aluno, novaQuestao)

        arquivoAluno = open(buildDir + '/' + nomeArquivoAluno, 'w')
        arquivoAluno.write(novaQuestao)
        arquivoAluno.close()

        arquivoAssinatura = open(buildDir + '/' + nomeDiretorioAluno + '/' + 'assinatura', 'w')
        arquivoAssinatura.write(assinatura)
        arquivoAssinatura.close()

        """ Copiando arquivo Makefile por aluno """
        with open('Makefile', 'r') as makefile:
            contentMakefile = makefile.read()
        makefile.close()
        contentMakefile = re.sub('exam.tex', templateFilenameDirectory + ".tex", contentMakefile)
        with open(buildDir + '/' + nomeDiretorioAluno + '/' + 'Makefile', 'w') as makefile:
            makefile.write(contentMakefile)
        makefile.close()

        """ Copiando as figuras """
        if 'figuras' in os.listdir(currentWorkDirectory):
            if 'figuras' in os.listdir(buildDir + '/' + nomeDiretorioAluno):
                shutil.rmtree(buildDir + '/' + nomeDiretorioAluno + '/' + 'figuras')
            shutil.copytree('figuras', buildDir + '/' + nomeDiretorioAluno + '/' + 'figuras')
        else:
            print 'Não foi possível encontrar o diretório figuras/'

        """ Gerando QR Codes """
        with open(buildDir + '/' + nomeDiretorioAluno + '/' + 'assinatura', 'r') as arquivoAssinatura:
            content = arquivoAssinatura.read()
        arquivoAssinatura.close()
        #print binascii.hexlify(content)
        #print binascii.unhexlify(binascii.hexlify(content))

        img = qrcode.make('http://192.168.0.12:8080/' + binascii.hexlify(content) + '/', image_factory=PilImage)
        img.save(buildDir + '/' + nomeDiretorioAluno + '/' + 'figuras/qrcode.png')







            # if len(todasQuestoes) > 0:
            #     questoes = todasQuestoes[:]
            #     shuffle(questoes)
            #     for questao in questoes:



