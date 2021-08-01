

/*
//   __________________
//  | ________________ |
//  ||                ||
//  ||[Testing Agenda]||
//  ||                ||
//  ||                ||
//  ||________________||
//  |__________________|B
//  \###################\U
//   \###################\N
//    \        ____       \N
//     \_______\___\_______\Y


- Validate topology length 
- Validate query the whole topolgies
- Validate query on components
- Validate deleting a topology
- vaildate components that connected to a given node


*/


const TopologyAPI = require('./');

describe('TopologyAPI test', () => {
    let topologyAPI;


/*

    Loop through all the avialable topologies

*/
    beforeEach(async() => {
        topologyAPI = new TopologyAPI();
        await topologyAPI.readJson('topology');
        await topologyAPI.readJson('topology1');
        await topologyAPI.readJson('topology2');
        await topologyAPI.readJson('topology3');

    });


    // Validate topology length 
    describe('readJson', () => {
        it('MUST be length 4', () => {
            expect(topologyAPI.topologies.length).toBe(4);
        })
    })


    // validate query the whole topolgies
    describe('queryTopologies', () => {
        it('MUST return all topologies', async() => {
            const result = await topologyAPI.queryTopologies();
            expect(result).toMatchObject(topologyAPI.topologies);
        })
    })

    // validate query on components
    describe('queryDevices', () => {
        it('MUST return topologies components', async() => {
            const result = await topologyAPI.queryDevices("top1");
            expect(result).toMatchObject(topologyAPI.topologies[0].components);
        })
    })


    // validate deleting a topology
    describe('deleteTopology', () => {
        it('MUST reduce length by one', async() => {
            await topologyAPI.deleteTopology("top1");
            expect(topologyAPI.topologies.length).toBe(3);
        })

        it('MUST return deleted topology', async() => {
            const result = await topologyAPI.deleteTopology("top1");
            expect(result.id).toBe("top1");
        })
    })




// vaildate components that connected to a given node
    describe('queryDevicesWithNetlistNode', () => {
        it('MUST return topologies components that connected to a given node', async() => {
            const result = await topologyAPI.queryDevicesWithNetlistNode("top1", "vss");
            expect(result).toMatchObject([topologyAPI.topologies[0].components[1]]);
        })
    })
});