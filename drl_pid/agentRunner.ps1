
        for ($i = 0; $i -lt 100; $i++) {
            try { python dqn_pid_discrete.py }
            catch { continue }    
        }

        for ($i = 0; $i -lt 100; $i++) {
            try { python sarsa_pid_discrete.py }
            catch { continue }    
        }

        for ($i = 0; $i -lt 100; $i++) {
            try { python cem_deep.py }
            catch { continue }    
        }

        for ($i = 0; $i -lt 100; $i++) {
            try { python pid.py }
            catch { continue }    
        }
