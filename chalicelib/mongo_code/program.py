from colorama import Fore
import program_hosts
import data.mongo_setup as mongo_setup


def main():
    mongo_setup.global_init()

    print_header()


    program_hosts.run()



def print_header():
    

    print(Fore.RED + '****************  Open Notif  ****************')
    print(Fore.GREEN )
    print("Welcome to open_Notif!")
    print()

if __name__ == '__main__':
    main()
