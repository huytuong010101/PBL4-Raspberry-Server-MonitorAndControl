class SocketService{
    static network_send = []
    static network_receive = []
    static cpu_total = []
    static temp = []
    static ansi_up = new AnsiUp

    constructor(address="ws://" + location.hostname + ":8000/6969"){
        this.address = address
        
    }

    init_socket(){
        this.ws = new WebSocket(this.address);
        this.ws.onclose = this.disconnect
        this.ws.onmessage = this.execute_event
        this.ws.onopen = () => {
            const data = {
                "event": "connect_ssh",
                "data": {}
            }
            this.ws.send(JSON.stringify(data))
        }
    }

    execute_event(response){
        response = JSON.parse(response.data)
        if (response["event"] && response["data"] && SocketService[response["event"]]){
            SocketService[response["event"]](response["data"])
        }
    }
    // All request here
    execute_command(command, cwd=null){
        const data = {
            "event": "execute_command",
            "data": {
                "command": command
            }
        }
        if (cwd){
            data["data"]["cwd"] = cwd
        }
        this.ws.send(JSON.stringify(data))
    }

    cancel_command(){
        const data = {
            "event": "cancel_command",
            "data": null
        }
        this.ws.send(JSON.stringify(data))
    }

    update_group(...groups){
        const data = {
            "event": "update_group",
            "data": {
                "groups": groups
            }
        }
        this.ws.send(JSON.stringify(data))
    }
    // All service here
    static update_resource(data){
        update_total_cpu(data.cpu.Total)
        SocketService.cpu_total.push(data.cpu.Total)
        if (SocketService.cpu_total.length > 20) SocketService.cpu_total.shift()

        //console.log(data)
        for (const core in data.cpu){
            if (core !=  "Total"){
                update_core(core, data.cpu[core])
            }
        }
        update_temperature(data.temperature)
        SocketService.temp.push(data.temperature)
        if (SocketService.temp.length > 20) SocketService.temp.shift()
        cpu_chart.updateSeries([
            {
              name: "CPU Performance",
              data: SocketService.cpu_total
            },
            {
              name: 'CPU Temperature',
              data: SocketService.temp
            }
        ])

        update_network(data.network.send, data.network.receive)
        SocketService.network_send.push(parseFloat(data.network.byte_send / 1024).toFixed(2))
        SocketService.network_receive.push(parseFloat(data.network.byte_receive / 1024).toFixed(2))
        if (SocketService.network_send.length > 20) SocketService.network_send.shift()
        if (SocketService.network_receive.length > 20) SocketService.network_receive.shift()
        network_chart.updateSeries([
            {
              name: "Network Send",
              data: SocketService.network_send
            },
            {
              name: 'Network Receive',
              data: SocketService.network_receive
            }
        ])

        update_memory(data.memory.Virtual.percent, data.memory.Swap.percent)
        
        update_disk(data.disk)

    }

    static response_command(data){
        const terminal_command = data.command.replaceAll("\n", "<br>")
        const html_command = SocketService.ansi_up.ansi_to_html(terminal_command)
        document.querySelector("#terminal-content").innerHTML += html_command.replaceAll("&lt;br&gt;", "<br>")
        document.querySelector("#terminal-screen").scrollTop = document.querySelector("#terminal-screen").scrollHeight 
        document.querySelector("#terminal-input").disabled = false
        document.querySelector("#terminal-input").focus()
    }

    disconnect(){
        toastr.error("Socket was disconnect", "Socket error")
        window.location.reload()
    }
}