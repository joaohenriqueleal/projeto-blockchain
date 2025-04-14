from blockchain import *


blockchain = Blockchain()

def main_menu():
    print('=' * 80)
    print('Gerenciador do BlockChain.'.center(80))
    print('=' * 80)
    while True:
        time.sleep(1)
        print('[1] para Adicionar um Block ao pending Blocks.')
        print('[2] para Adicionar uma Transação ao pending Block atual.')
        print('[3] para Minerar o pending Block atual.')
        print('[4] para Ver o Blockchain.')
        print('[5] para Consultar a dificuldade de mineração atual.')
        print('[6] para Verificar a integridade do Blockchain.')
        print('[7] para Sair.')
        print('-' * 80)
        try:
            opcao = int(input('>>>  '))
            print('-' * 80)
        except:
            print('\033[;31mDigite um inteiro válido!\033[m')
            continue
        if opcao == 1:
            block = Block(blockchain.get_index(), blockchain.get_previous_hash(), blockchain.difficulty)
            blockchain.add_block_to_pending(block)
            print(f'Bloco {blockchain.pending_blocks[0].index} adicionado ao pending!')
            print('-' * 80)
        elif opcao == 2:
            try:
                sender = str(input('Remetente: ')).strip()
                receiver = str(input('Destinatário: ')).strip()
                value = float(input('Valor da transação: '))
                transaction = Transaction(sender, receiver, value)
                print('-' * 80)
                if not blockchain.pending_blocks:
                    print('\033[;31mVoce precisa adicionar um bloco ao pending primeiro!\033[m')
                    continue
                blockchain.pending_blocks[0].add_transaction(transaction)
                print(f'Transação de hash: {transaction.transaction_hash} adicionada ao bloco: {blockchain.pending_blocks[0].index}')
                print('-' * 80)
            except:
                print('\033[;31mDigite um valor válido!\033[m')
                continue
        elif opcao == 3:
            if len(blockchain.pending_blocks) > 0:
                threading.Thread(target=blockchain.pending_blocks[0].mine_block()).start()
            else:
                print('\033[;31mAdicione um bloco a ser minerado primeiro!\033[m')
            print('-' * 80)
        elif opcao == 4:
            blockchain.print_chain()
            print('-' * 80)
        elif opcao == 5:
            print(f'Dificuldade de mineração atual: {blockchain.difficulty}')
            print('-' * 80)
        elif opcao == 6:
            integridade = ''
            if blockchain.chain_is_valid(): integridade = 'Sim!'
            else: integridade = 'Não!'
            print(f'Blockchain está integra? {integridade}')
            print('-' * 80)
        elif opcao == 7:
            print('Obrigado! Volte Sempre!')
            exit()
        else:
            print('\033[;31mDigite um inteiro de 1 a 6!')
        blockchain.adjust_difficulty()

if __name__ == '__main__':
    main_menu()
