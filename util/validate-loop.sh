while [ 1 ]
do

        # in a loop
        mkdir -p tmp

        mapfile -t array < <(python src/finalexperiment.py --no-info --netem-down --netem-up --validate --output-dir tmp)

        houseid=$(echo ${array[2]} | cut -d' ' -f8 | cut -d'-' -f2 | cut -d'.' -f1)

        # uplink
        sudo tc qdisc del dev $(ip route get 10.0.0.0 | head -n 1 | cut -d \  -f4) root
        eval "${array[0]}"

        # downlink
        ssh $USER@server "sudo tc qdisc del dev $(ip route get 10.0.0.0 | head -n 1 | cut -d \  -f4) root"
        ssh $USER@server "${array[1]}"

        bash util/validate.sh
        bash util/consolidate-validation-results.sh > tmp/"consolidate-$houseid".csv

        mv tmp "tmp-$houseid"
done

