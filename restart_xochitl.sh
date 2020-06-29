kill -9 $(ps | grep [x]ochitl | awk 'NR==1{print $1}')
