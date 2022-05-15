import boto3

# Create a CLASSIC Load Balancer
def elb_manager(InstanceIds, sgId):
    elb = boto3.client('elb')

    lbl=elb.create_load_balancer(
        LoadBalancerName='nixlb2',
        Listeners=[
            {
                'Protocol':'HTTP',
                'LoadBalancerPort':80,
                'InstanceProtocol':'HTTP',
                'InstancePort':80
            },
        ],
        AvailabilityZones=['eu-west-1a',]
    )

    DNSName=lbl['DNSName']
    print(DNSName)

    # Apply the security Group
    elb.apply_security_groups_to_load_balancer(
        LoadBlancerName='nixlb2',
        # TODO: sgId como una lista no como un valor. requiere cambios en main
        SecurityGroups=[sgId]
    )

    health_check=elb.configure_health_check(
        LoadBalancerName='nixlb2',
        HealthCheck={
            # 'Target':'HTTP:80/index.html'
            'Target':'TCP:22',
            'Interval':10, # En segundos
            'Timeout':5, # En segundos, debe ser menor que Interval
            'UnhealthyThreshold':5, # es el numero de fallos consecutivos antes de poner la instancia como fallida
            'HealthyThreshold': 5 # es el numero de exitos consecutivos antes de poner la instancia como disponible
        }
    )

    # Attach an instance
    attachinst=elb.register_instances_with_load_balancer(
        LoadBalancerName='nixlb2',
        Instances=InstanceIds
    )