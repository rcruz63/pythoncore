import boto3

# Create a CLASSIC Load Balancer
def elb_manager(Name, InstanceIds, sgId, AZ):
    elb = boto3.client('elb')

    lbl=elb.create_load_balancer(
        LoadBalancerName='lb'+Name,
        Listeners=[
            {
                'Protocol':'HTTP',
                'LoadBalancerPort':80,
                'InstanceProtocol':'HTTP',
                'InstancePort':80
            },
        ],
        AvailabilityZones=AZ
    )

    DNSName=lbl['DNSName']
    print(DNSName)

    # Apply the security Group
    elb.apply_security_groups_to_load_balancer(
        LoadBalancerName='lb'+Name,
        # TODO: sgId como una lista no como un valor. requiere cambios en main
        SecurityGroups=sgId
    )

    health_check=elb.configure_health_check(
        LoadBalancerName='lb'+Name,
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
        LoadBalancerName='lb'+Name,
        Instances=InstanceIds
    )

    print(attachinst)

    input("Presiona una tecla para desregistrar las instancias")
    elb.deregister_instances_from_load_balancer(
        LoadBalancerName='lb'+Name,
        Instances=InstanceIds
    )

    input("Presiona una tecla para eliminar el Load Balancer")
    elb.delete_load_balancer(LoadBalancerName='lb'+Name)