        path = 'C:/Users/lavisht/AppData/Local/Programs/Python/Python38/Lib/site-packages/pid_env/drl_pid/dsc/dqn/*'
        list_of_files = glob.glob(path) # * means all if need specific format then *.csv

        mean_df = []

        for file in list_of_files:
            a = pd.read_csv(file)    
            a['error'] = abs(a['sp'] - a['pv'])
            
            first_transition = a.head(1500).tail(1000)
            first_transition_mean = first_transition["error"].mean()
            #print("first transition mean : " , mean)
                
            last_transition = a.tail(1000)
            last_transition_mean = last_transition["error"].mean()  
            #print("last transition mean : " , mean)
            
            mean_df.append([first_transition_mean,last_transition_mean])
            

        mean_df = pd.DataFrame(mean_df, 
        columns=['first_transition_mean', 
                'last_transition_mean'])

        print("first_transition_mean : ", 
        mean_df['first_transition_mean'].mean() )
        print("last_transition_mean : ", 
        mean_df['last_transition_mean'].mean() )
        print("first_transition_median : ", 
        mean_df['first_transition_mean'].median() )
        print("last_transition_median : ", 
        mean_df['last_transition_mean'].median() )
        print("max_of_first_transition_mean : ", 
        mean_df['first_transition_mean'].max() )
        print("max_of_last_transition_mean : ", 
        mean_df['last_transition_mean'].max() )
        print("min_of_first_transition_mean : ", 
        mean_df['first_transition_mean'].min() )
        print("min_of_last_transition_mean : ", 
        mean_df['last_transition_mean'].min() )

        print("count_of_ft_mean_above_median : ",
        mean_df[mean_df['first_transition_mean']
        .gt(ft_median)]['first_transition_mean'].count() )
        print("count_of_ft_mean_below_median : ",
        mean_df[mean_df['first_transition_mean']
        .lt(ft_median)]['first_transition_mean'].count() )

        print("count_of_lt_mean_above_median : ",
        mean_df[mean_df['last_transition_mean']
        .gt(lt_median)]['last_transition_mean'].count() )
        print("count_of_lt_mean_below_median : ",
        mean_df[mean_df['last_transition_mean']
        .lt(lt_median)]['last_transition_mean'].count() )
