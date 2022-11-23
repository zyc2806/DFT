# pymatgen_usage_Chinese

- **Side-note : as_ dict / from_ dict**
    
    Pymatgen的as_dict提供了一种以更好的方式保存你的工作的方法。
    
    as_dict方法的输出总是可序列化的json/yaml。因此，如果你想保存一个结构：
    
    ```python
    with open('structure.json','w')as f:
        json.dump(structure.as_dict(), f)
    ```
    
    可以按以下方法从json中恢复结构（或任何有as_dict方法的对象）
    
    ```python
    with open('structure.json', 'r')as f:
        d = json.load(f)
        structure = Structure.from_dict(d)
    ```
    
    - **MontyEncoder/Decode**
        
        要使用MontyEncoder，只需在使用json时将其作为cls kwarg加入
        
        ```python
        json.dumps(object, cls=MontyEncoder)
        ```
        
        MontyDecoder依赖于在dict中找到一个"@module "和"@class "键来解码必要的python对象。一般来说，如果这些键不存在，MontyEncoder会添加这些键，但是为了更好的长期稳定性（例如，可能存在直接调用to_dict而不是通过编码器的情况），最简单的方法是在任何to_dict属性中添加以下内容。
        
        ```python
        d["@module"] = type(self).__module__
        d["@class"] = type(self).__name__
        ```
        
        要使用MontyDecoder，只需在使用json加载时将其指定为cls kwarg，例如：
        
        ```python
        json.loads(json_string, cls=MontyDecoder)
        ```
        
        MontyEncoder/Decoder也支持日期时间和numpy数组。
        
    
- **Structures and Molecules**
    
    有几种方法来创建结构与分子对象：
    
    - **手动创建结构**
        
        手动创建晶体结构，使用较少，以下为创建Si晶体的代码：
        
        ```python
        from pymatgen.coreimport Lattice, Structure, Molecule
        
        coords = [[0, 0, 0], [0.75,0.5,0.75]]
        lattice = Lattice.from_parameters(a=3.84, b=3.84, c=3.84, alpha=120,
                                          beta=90, gamma=60)
        struct = Structure(lattice, ["Si", "Si"], coords)
        
        coords = [[0.000000, 0.000000, 0.000000],
                  [0.000000, 0.000000, 1.089000],
                  [1.026719, 0.000000, -0.363000],
                  [-0.513360, -0.889165, -0.363000],
                  [-0.513360, 0.889165, -0.363000]]
        methane = Molecule(["C", "H", "H", "H", "H"], coords)
        ```
        
        元素的基态离子态均有效，如Fe与Fe2+。
        
    - **读和写结构/分子文件**
        
        通常使用典型格式的结构/分子（如CIF、电子结构代码输入/输出、xyz、mol等）来创建结构，Pymatgen通过from_file和to方法提供了一个方便的方法来读取结构和分子。
        
        ```python
        # Read a POSCAR and write to a CIF.
        structure = Structure.from_file("POSCAR")
        structure.to(filename="CsCl.cif")
        
        # Read an xyz file and write to a Gaussian Input file.
        methane = Molecule.from_file("methane.xyz")
        methane.to(filename="methane.gjf")
        ```
        
        格式是由文件名自动猜测。
        
        为了更精细地控制要使用的结构格式，你可以指定特定的io包。例如，要从一个cif创建一个结构：
        
        ```python
        from pymatgen.io.cif import CifParser
        parser = CifParser("mycif.cif")
        structure = parser.get_structures()[0]
        ```
        
        从VASP的POSCAR/CONTCAR文件创建一个结构。
        
        ```python
        from pymatgen.io.vasp import Poscar
        poscar = Poscar.from_file("POSCAR")
        structure = poscar.structure
        ```
        
        许多这些io包还提供了将结构体写成各种输出格式的方法，例如`pymatgen.io.cif`中的CifWriter。
        
        值得一提，`pymatgen.io.vasp.set`提供了一种方法，可以从一个结构中生成完整的VASP输入文件集。
        
        例如，读取一个POSCAR和写入一个CIF：
        
        ```python
        from pymatgen.io.vasp import Poscar
        from pymatgen.io.cif import CifWriter
        
        p = Poscar.from_file('POSCAR')
        w = CifWriter(p.structure)
        w.write_file('mystructure.cif')
        ```
        
        对于分子，pymatgen通过`pymatgen.io.xyz`和`pymatgen.io.gaussian`分别内置了对XYZ和高斯输入和输出文件的支持。
        
        ```python
        from pymatgen.io.xyz import XYZ
        from pymatgen.io.gaussian import GaussianInput
        
        xyz = XYZ.from_file('methane.xyz')
        gau = GaussianInput(xyz.molecule,
                            route_parameters={'SP': "", "SCF": "Tight"})
        gau.write_file('methane.inp')
        ```
        
        通过OpenBabel接口支持100多种文件类型。但这需要你安装带有Python绑定的openbabel[安装方法](https://pymatgen.org/installation.html)
        
    - **你可以用结构做的**
        
        可以参考的操作
        
        1. 直接修改结构，使用`pymatgen .transformations`和`pymatgen.alchemy`包。
        2. 分析结构。例如，使用`pymatgen.analysis.ewald`包计算Ewald和，使用`pymatgen.analysis.structure_matcher`比较两个结构的相似性。
        
        Structure和Molecule被设计为可变的，它们是最基本的可变单元（在类的层次结构中，所有下面的单元如Element、Specie、Site、PeriodicSite、Lattice都是不可变的）。如果需要保证结构/分子的不可变性，应使用IStructure和IMolecule类来代替。
        
        - **修改结构或分子**
            
            Pymatgen支持一个高度Pythonic的界面来修改结构和分子。例如，你可以简单地用以下方法改变任何部位：
            
            ```python
            # 将第1位改为氟原子。
            structure[1] = "F"
            molecule[1] = "F"
            
            # 改变元素和坐标（结构假设为分数坐标,
            # 分子为笛卡尔坐标。）
            structure[1] = "Cl", [0.51, 0.51, 0.51]
            molecule[1] = "F", [1.34, 2, 3]
            
            # 结构/分子也支持典型的列表式操作符,
            # 例如 reverse, extend, pop, index, count.
            structure.reverse()
            molecule.reverse()
            
            structure.append("F", [0.9, 0.9, 0.9])
            molecule.append("F", [2.1, 3,.2 4.3])
            ```
            
            还可以在Structures上做一些典型的变换：
            
            ```python
            # 构建超胞
            structure.make_supercell([2, 2, 2])
            
            # 获取结构的原始版本
            structure.get_primitive_structure()
            
            # 在两个结构之间进行插值，得到10个结构，通常用于NEB。
            structure.interpolate(another_structure, nimages=10)
            ```
            
            以上只是一些典型使用案例的例子，还有很多其他应用可以参考Structure和molecule的API文档。
            
- **Entries - 基本分析单元**
    
    除了核心的Element, Site和Structure外，pymatgen中的大多数分析（例如，创建相位图）都是通过Entry对象进行的。一个条目的最基本形式是包含一个计算能量和一个成分，并可以选择包含其他输入或计算数据。在大多数情况下，你将使用 `pymatgen. entries.computed_entries` 中定义的 ComputedEntry 或 ComputedStructureEntry 对象。ComputedEntry 对象可以通过手动解析计算数据计算，或者使用 `pymatgen.apps.borg` 包来创建。
    
    - **Compatibility- Mixing GGAand GGA+U runs**
        
        Ceder小组开发了一个方案，通过GGA和GGA+U计算可以 "混合"，这样就可以使用最适合每个结构的计算类型进行分析。
        
        例如，为了生成Fe-P-O相图，金属相如Fe和FexPy最适合使用标准的GGA建模，而Hubbard U应该应用于氧化物，如FexOy和FexPyOz。
        
        在`pymatgen.io.vasp.set`模块中，预定义的参数集已被编码，以允许用户生成与材料项目数据兼容的输入参数一致的VASP输入文件。希望使用这些参数计算的运行进行分析的用户应使用适当的兼容性对这些运行产生的条目进行后处理。例如，如果用户希望从Fe-P-O vasp运行生成的条目列表中生成相图，他应该使用以下程序。
        
        ```python
        from pymatgen.entries.compatibility import MaterialsProjectCompatibility
        from pymatgen.analysis.phase_diagram import PhaseDiagram, PDPlotter
        
        # 使用pymatgen.borg或其他方式获得未处理的条目。
        
        # 处理条目的兼容性
        compat = MaterialsProjectCompatibility()
        processed_entries = compat.process_entries(unprocessed_entries)
        
        # 这几行是使用ComputedEntries生成的相图。
        pd = PhaseDiagram(processed_entries)
        plotter = PDPlotter(pd)
        plotter.show()
        ```
        
- **`pymatgen.io`- 管理计算输入和输出**
    
    pymatgen.io模块包含一些类，以方便从各种计算代码中编写输入文件和解析输出文件，包括VASP、Q-Chem、LAMMPS、CP2K、AbInit等等。
    
    管理输入的核心类是`InputSet`。一个`InputSet`对象包含为一个计算写一个或多个输入文件所需的所有数据。具体来说，每个InputSet都有一个write_input()方法，可以将所有必要的文件写到你指定的位置。还有`InputGenerator`类，它产生的`InputSet`具有针对特定计算类型的设置（例如，结构弛豫）。你可以把`InputGenerator`类看作是完成特定计算任务的 "配方"，而`InputSet`则包含应用于特定系统或结构的这些配方。
    
    自定义设置可以在实例化时提供给`InputGenerator`。例如，使用Packmol代码构建一个用于将水分子包装到盒子里的`InputSet`，同时将包装公差从2.0（默认）改为3.0。
    
    ```python
    from pymatgen.io.packmol import PackmolBoxGen
    
    input_gen = PackmolBoxGen(tolerance=3.0)
    packmol_set = input_gen.get_input_set({"name": "water",
                                           "number": 500,
                                           "coords": "/path/to/input/file.xyz"})
    packmol_set.write_input('/path/to/calc/directory')
    ```
    
    你也可以使用`InputSet.from_directory()`从一个包含计算输入的目录中构建一个pymatgen `InputSet`。
    
    许多代码还包含用于将输出文件解析为pymatgen对象的类，这些类继承自`InputFile`，它提供了一个读写单个文件的标准接口。
    
    对`InputFile`、`InputSet`和`InputGenerator`类的使用还没有被pymatgen支持的所有代码完全实现，所以请参考每个代码各自的模块文档以了解更多细节。
    
- ****`pymatgen.borg`- 高通量数据**
    
    基本概念是提供一种方便的手段来同化目录结构中的大量数据。目前，主要的应用是将VASP计算的整个目录结构同化为可用的pymatgen条目，然后可以用于相图和其他分析。它的工作原理概要如下。
    
    1. Drones是在`pymatgen.app.borg.hive`模块中定义的。Drone本质上是一个对象，它定义了一个目录如何被解析成一个pymatgen对象。例如，VaspToComputedEntryDrone定义了一个包含vasp运行（有vasprun.xml文件）的目录如何被转换为ComputedEntry
    2. `pymatgen.app.borg.queen`模块中的BorgQueen对象使用Drones来同化整个子目录结构。在可能的情况下，使用并行处理来加速这一过程。
    - **简单的例子--绘制相图**
        
        假设你想制作Li-O相图。你已经计算了所有你感兴趣的Li、O和Li-O化合物，并且这些运行都在 "Li-O_runs "目录中。然后你可以使用下面几行代码来生成相图。
        
        ```python
        from pymatgen.borg.hive import VaspToComputedEntryDrone
        from pymatgen.borg.queen import BorgQueen
        from pymatgen.analysis.phase_diagram import PhaseDiagram, PDPlotter
        
        # 这三行将数据导入为ComputedEntries。
        drone = VaspToComputedEntryDrone()
        queen = BorgQueen(drone, "Li-O_runs", 2)
        entries = queen.get_data()
        
        # 执行save_data是个好主意，尤其是当你导入大量的数据而花费了一些时间。这允许你使用一个只用drone argument的BorgQueen来重新加载数据，并且调用 queen.load_data("Li-O_entries.json")
        queen.save_data("Li-O_entries.json")
        
        # 这几行是使用ComputedEntries生成的相图。
        pd = PhaseDiagram(entries)
        plotter = PDPlotter(pd)
        plotter.show()
        ```
        
        在这个例子中，Li和O都不需要Hubbard U。然而，如果你要从GGA和GGA+U的混合条目中制作相图，你可能需要在运行相图代码之前用兼容性对象对同化的条目进行后处理。见前面关于条目和兼容性的部分。
        
    - **另一个例子--计算反应能量**
        
        另一个例子是，你可以用加载的条目做一件很酷的事情，就是计算反应能量。例如，重新使用我们在上述步骤中保存的Li-O数据。
        
        ```python
        from pymatgen.apps.borg.hive import VaspToComputedEntryDrone
        from pymatgen.apps.borg.queen import BorgQueen
        from pymatgen.analysis.reaction_calculator import ComputedReaction
        
        # 这三行将数据同化为ComputedEntries。
        drone = VaspToComputedEntryDrone()
        queen = BorgQueen(drone)
        queen.load_data("Li-O_entries.json")
        entries = queen.get_data()
        
        #提取正确的条目并计算出反应。
        rcts = filter(lambda e: e.composition.reduced_formulain ["Li", "O2"], entries)
        prods = filter(lambda e: e.composition.reduced_formula == "Li2O", entries)
        rxn = ComputedReaction(rcts, prods)
        print rxn
        print rxn.calculated_reaction_energy
        ```
        
- **`pymatgen.transformations`**
    
    `pymatgen.transformations`包是用于对结构进行转换的标准包。目前已经支持许多转换，从简单的转换，如添加和删除位点，替换结构中的物种，到更高级的一对多的转换，如使用静电能量准则从结构中部分删除某个物种的一部分。转换类遵循一个严格的API。一个典型的例子如下：
    
    ```python
    from pymatgen.io.cif import CifParser
    from pymatgen.transformations.standard_transformations import RemoveSpecieTransformations
    
    # 从cif中读入LiFePO4结构。
    parser = CifParser('LiFePO4.cif')
    struct = parser.get_structures()[0]
    
    t = RemoveSpeciesTransformation(["Li"])
    modified_structure = t.apply_transformation(struct)
    ```
    
- **`pymatgen.alchemy` - 高通量转换**
    
    `pymatgen.alchemy`包是一个用于进行高通量（HT）结构转化的框架。例如，它允许用户定义一系列应用于一组结构的转换，在此过程中产生新的结构。该框架还被设计为对所有在结构上进行的改变进行适当的记录，并有无限的撤销。主要的类是：
    
    1. `pymatgen.alchemy.materials.TransformedStructure` - 代表 TransformedStructure 的标准对象。接收一个输入结构和一个转换列表作为输入。也可以从cifs和POSCARs生成。
    2. `pymatgen.alchemy.transmuters.StandardTransmuter` - Transmuter类的一个例子，它接收一个结构列表，并在所有结构上应用一系列的转换。
    
    ```python
    from pymatgen.alchemy.transmuters import CifTransmuter
    from pymatgen.transformations.standard_transformations import SubstitutionTransformation, RemoveSpeciesTransformation
    
    trans = []
    trans.append(SubstitutionTransformation({"Fe":"Mn"}))
    trans.append(RemoveSpecieTransformation(["Lu"]))
    transmuter = CifTransmuter.from_filenames(["MultiStructure.cif"], trans)
    structures = transmuter.transformed_structures
    ```
    
- **`pymatgen.matproj.rest` - 与Materials Project REST API集成**
    
    在pymatgen的2.0.0版本后，引入了一个最强大和有用的工具-Materials Project REST API的适配器。Materials Project  REST API（简称Materials API）的引入是为了给用户提供一种程序化查询材料数据的方法。这使用户无需通过网络界面有效地进行结构操作和分析。
    
    同时，我们在`pymatgen.ext.matproj`模块中编码了MPRester，这是一个用户友好的材料API的高级接口，用于获取有用的pymatgen对象，以便进一步分析。要使用Materials API，你需要首先在Materials Project 中注册，并在你的仪表板上生成你的API密钥，网址是[https://www.materialsproject.org/dashboard](https://www.materialsproject.org/dashboard)。在下面的例子中，用户的材料API密钥被指定为 "USER_API_KEY"。
    
    MPRester提供了许多方便的方法，但我们在这里只强调几个关键的方法。
    
    要获得材料项目编号为 "mp-1234 "的材料的信息，可以使用以下方法。
    
    ```python
    from pymatgen.ext.matproj import MPRester
    with MPRester("USER_API_KEY")as m:
    
    # 结构
    structure = m.get_structure_by_material_id("mp-1234")
    
    # Dos
    dos = m.get_dos_by_material_id("mp-1234")
    
    # Bandstructure
    bandstructure = m.get_bandstructure_by_material_id("mp-1234")
    ```
    
    材料API还允许通过公式查询数据:
    
    ```python
    # 要获得分子式为Fe2O3的所有条目的数据列表
    data = m.get_data("Fe2O3")
    
    # 得到所有分子式为Fe2O3的条目的能量
    energies = m.get_data("Fe2O3", "energy")
    ```
    
    最后，MPRester 提供了获得一个化学系统中所有条目的方法。与brog框架相结合，这为将自己的计算结果与材料项目数据结合起来进行分析提供了一种特别强大的方法。下面的代码展示了如何确定一种新的计算材料的相稳定性。
    
    ```python
    from pymatgen.ext.matproj import MPRester
    from pymatgen.apps.borg.hive import VaspToComputedEntryDrone
    from pymatgen.apps.borg.queen import BorgQueen
    from pymatgen.entries.compatibility import MaterialsProjectCompatibility
    from pymatgen.analysis.phase_diagram import PhaseDiagram, PDPlotter
    
    # 将VASP计算结果同化为ComputedEntry对象。我们假设计算的是一系列新的LixFey0z相，我们想知道相的稳定性。
    drone = VaspToComputedEntryDrone()
    queen = BorgQueen(drone, rootpath=".")
    entries = queen.get_data()
    
    # 使用材料项目REST API获得所有现有的Li-Fe-O相
    with MPRester("USER_API_KEY")as m:
        mp_entries = m.get_entries_in_chemsys(["Li", "Fe", "O"])
    
    # 从计算运行的条目与材料项目的条目结合起来
    extend(mp_entries)
    
    # 使用MaterialsProjectCompatibility处理条目
    compat = MaterialsProjectCompatibility()
    entries = compat.process_entries(entries)
    
    # 生成并绘制Li-Fe-O相图
    pd = PhaseDiagram(entries)
    plotter = PDPlotter(pd)
    plotter.show()
    ```
    
    - **查询方法**
        
        为了获得最大的灵活性，你也可以使用MPRester的查询方法。该方法允许对材料项目数据库进行任何类型的mongo查询。它还支持带有通配符的简单字符串语法。下面给出了一些例子。
        
        ```python
        from pymatgen.ext.matproj import MPRester
        
        with MPRester("USER_API_KEY")as m:
        
        # 获取分子式为 "*2O "的材料的所有能量。
        results = m.query("*2O", ['energy'])
        
        # 获取材料名称为mp-1234的材料的分子式和能量或分子式为Fe0的材料。
        or with formula Fe0.results = m.query("FeO mp-1234", ['pretty_formula', 'energy'])
        
        # 获取所有形式为ABO3的化合物
        results = m.query("**O3", ['pretty_formula', 'energy'])
        ```
        
        建议查阅材料API文档，网址是[http://bit.ly/materialsapi](http://bit.ly/materialsapi)，该文档对材料项目中使用的文件模式以及如何最好地查询你所需要的相关信息进行了全面的解释。
        
    - **在confg fle中设置PMG_MAPI_KEY。**
        
        MPRester也可以通过pymatgen配置文件读取API密钥。只需运行：
        
        `pmg config --add PMG_MAPI_KEY <USER_API_KEY>`
        
        将其添加到 .pmgrc.yaml 中，现在你可以在没有任何参数的情况下调用 MPRester。这使得Materials API的大量用户更容易使用MPRester，而不必在脚本中不断插入他们的API密钥。
        
- S**ome Sample Example**
    
    ```python
    import pymatgen.core as mg
    si = mg.Element("Si")
    si.atomic_mass
    ```
    
    `28.0855`
    
    ```python
    print(si.melting_point)
    ```
    
    `1687.0 K`
    
    ```python
    comp = mg.Composition("Fe2O3")
    comp.weight
    ```
    
    `159.6882`
    
    ```python
    # 可以直接使用元素符号代替元素
    comp["Fe"]
    ```
    
    `2.0`
    
    ```python
    comp.get_atomic_fraction("Fe")
    ```
    
    `0.4`
    
    ```python
    lattice = mg.Lattice.cubic(4.2)
    structure = mg.Structure(lattice, ["Cs", "Cl"],
                             [[0, 0, 0], [0.5, 0.5, 0.5]])
    structure.volume
    ```
    
    `74.088000000000008`
    
    ```python
    structure[0]
    ```
    
    `PeriodicSite: Cs (0.0000, 0.0000, 0.0000) [0.0000, 0.0000, 0.0000]`
    
    ```python
    # 使用空间群对称性创建一个结构。
    li2o = mg.Structure.from_spacegroup("Fm-3m", mg.Lattice.cubic(3),
                                            ["Li", "O"],
                                            [[0.25, 0.25, 0.25], [0, 0, 0]])
    # 来自spglib的综合对称性分析工具。
    frompymatgen.symmetry.analyzerimport SpacegroupAnalyzer
    finder = SpacegroupAnalyzer(structure)
    finder.get_space_group_symbol()
    ```
    
    `'Pm-3m'`
    
    ```python
    # 方便地输入各种格式。你可以指定各种文件格式。如果没有文件名，将返回一个字符串。
    # 否则，输出被写入文件。如果只提供了文件名，格式将从文件中确定。
    structure.to(fmt="poscar")
    structure.to(filename="POSCAR")
    structure.to(filename="CsCl.cif")
    ```
    
    ```python
    # 读取结构文件也同样简单
    structure = mg.Structure.from_str(open("CsCl.cif").read(), fmt="cif")
    structure = mg.Structure.from_file("CsCl.cif")
    ```
    
    ```python
    # 从文件中读取和写入分子。默认支持XYZ和高斯的输入和输出。 
    # 通过可选的openbabel（如果已安装）支持许多其他格式。
    methane = mg.Molecule.from_file("methane.xyz")
    mol.to("methane.gjf")
    ```
    
    ```python
    # 用于编辑结构和分子的Pythonic API（v2.9.1以上） 改变位点的元素。
    structure[1] = "F"
    print(structure)
    ```
    
    ```python
    Structure Summary (Cs1 F1)
    Reduced Formula: CsF
    abc   :   4.200000   4.200000   4.200000
    angles:  90.000000  90.000000  90.000000
    Sites (2)
    1 Cs     0.000000     0.000000     0.000000
    2 F     0.500000     0.500000     0.500000
    ```
    
    ```python
    # 改变物种和坐标（对structure而言，假设是分数）。
    structure[1] = "Cl", [0.51, 0.51, 0.51]
    print(structure)
    ```
    
    ```python
    Structure Summary (Cs1 Cl1)
    Reduced Formula: CsCl
    abc   :   4.200000   4.200000   4.200000
    angles:  90.000000  90.000000  90.000000
    Sites (2)
    1 Cs     0.000000     0.000000     0.000000
    2 Cl     0.510000     0.510000     0.510000
    ```
    
    ```python
    # 用K取代结构中的所有Cs
    structure["Cs"] = "K"
    print(structure)
    ```
    
    ```python
    Structure Summary (K1 Cl1)
    Reduced Formula: KCl
    abc   :   4.200000   4.200000   4.200000
    angles:  90.000000  90.000000  90.000000
    Sites (2)
    1 K     0.000000     0.000000     0.000000
    2 Cl     0.510000     0.510000     0.510000
    ```
    
    ```python
    # 用K:0.5, Na:0.5替换结构中的所有K，即创建一个无序的结构。
    structure["K"] = "K0.5Na0.5"
    print(structure)
    ```
    
    ```python
    Full Formula (K0.5 Na0.5 Cl1)
    Reduced Formula: K0.5Na0.5Cl1
    abc   :   4.209000   4.209000   4.209000
    angles:  90.000000  90.000000  90.000000
    Sites (2)
      #  SP                   a    b    c
    ---  -----------------  ---  ---  ---
      0  K:0.500, Na:0.500  0    0    0
      1  Cl                 0.5  0.5  0.5
    ```
    
    ```python
    # 因为结构像一个列表，所以它支持大多数类似列表的方法，如排序、反向等。
    structure.reverse()
    print(structure)
    ```
    
    ```python
    Structure Summary (Cs1 Cl1)
    Reduced Formula: CsCl
    abc   :   4.200000   4.200000   4.200000
    angles:  90.000000  90.000000  90.000000
    Sites (2)
    1 Cl     0.510000     0.510000     0.510000
    2 Cs     0.000000     0.000000     0.000000
    ```
    
    ```python
    # 分子的功能类似，但有站点和笛卡尔坐标。 以下是将CH4中的C变为N，并在X方向上移动了0.0lA。
    methane[0] = "N", [0.01, 0, 0]
    ```