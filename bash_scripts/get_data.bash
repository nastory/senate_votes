for CONGRESS in `seq 101 117`; 
do for SESSION in 1 2; 
do `wget "https://www.senate.gov/legislative/LIS/roll_call_lists/vote_menu_${CONGRESS}_${SESSION}.xml"`;
done;
done