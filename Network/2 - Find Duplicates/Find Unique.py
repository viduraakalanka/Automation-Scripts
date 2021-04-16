def find_unique():
    with open('Dup_Val.txt', 'r') as f:
        #ip_list = [line.strip() for line in f]  
        dup_ip_list = f.readlines()
        
    uniq_ip_list = set(dup_ip_list)
    print uniq_ip_list
    
    output_file = open('Unique_Val.txt','w')
    for ip in uniq_ip_list:
        output_file.write(ip)

    output_file.close()

find_unique()
