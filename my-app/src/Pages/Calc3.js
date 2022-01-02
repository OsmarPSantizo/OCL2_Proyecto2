import React from "react";
import {Bar} from 'react-chartjs-2'

function Calc3(){
    return(
        <div>
            <h1 className="Calc">Indice de Progresión de la pandemia.</h1>
            <Bar
            data={{
              labels: ['Red', 'Blue'],
              
              datasets:[
                  {
                  label: '# de votos',
                  data: [12,19,3,5,2,3],
                  backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                  ],
                  borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1

                }]

            }}
        
            options={{
                maintainAspectRatio:false,
                scales:{
                    y:[
                        {
                        ticks:{
                            beginAtZero:true
                        },
                    },
                    ],
                }
            }}
            />
        </div>
    );

}

export default Calc3;