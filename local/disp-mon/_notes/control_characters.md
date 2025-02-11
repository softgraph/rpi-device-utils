# Control Characters and Sequences

## Terms

### CL, CR, GL, and GR (ECMA-35)

- Area Table:

| Code Range | Area Name | Description |
|------------|-----------|-------------|
| 0x00-0x1F  | `CL`      | Control characters Left |
| 0x20-0x7F  | `GL`      | Graphic characters Left |
| 0x80-0x9F  | `CR`      | Control characters Right |
| 0xA0-0xFF  | `GR`      | Graphic characters Right |

### C0 Code Set (ECMA-48)

- Mapped to `CL` Area (0x00-0x1F)

- Code Table:

| Code | Name  | Description |
|------|-------|-------------|
| 0x00 | `NUL` | Null        |
| 0x01 | `SOH` | Start of Heading |
| 0x02 | `STX` | Start of Text |
| 0x03 | `ETX` | End of Text |
| 0x04 | `EOT` | End of Transmission |
| 0x05 | `ENQ` | Enquiry     |
| 0x06 | `ACK` | Acknowledgement |
| 0x07 | `BEL` | Bell        |
| 0x08 | `BS`  | Backspace   |
| 0x09 | `HT`  | Horizontal Tabulation (Character Tabulation) |
| 0x0A | `LF`  | Line Feed   |
| 0x0B | `VT`  | Vertical Tabulation |
| 0x0C | `FF`  | Form Feed   |
| 0x0D | `CR`  | Carriage Return |
| 0x0E | `SO`  | Shift Out (7-bit) |
|      | `LS1` | Locking Shift One (8-bit) |
| 0x0F | `SI`  | Shift In (7-bit) |
|      | `LS0` | Locking Shift Zero (8-bit) |
| 0x10 | `DLE` | Data Link Escape |
| 0x11 | `DC1` | Device Control 1 |
| 0x12 | `DC2` | Device Control 2 |
| 0x13 | `DC3` | Device Control 3 |
| 0x14 | `DC4` | Device Control 4 |
| 0x15 | `NAK` | Negative Acknowledgement |
| 0x16 | `SYN` | Synchronous Idle |
| 0x17 | `ETB` | End of Transmission Block |
| 0x18 | `CAN` | Cancel      |
| 0x19 | `EM`  | End of Medium |
| 0x1A | `SUB` | Substitute  |
| 0x1B | `ESC` | Escape      |
| 0x1C | `IS4` | Information Separator Four |
|      | `FS`  | File Separator |
|      | `DT`  | Document Terminator |
| 0x1D | `IS3` | Information Separator Three |
|      | `GS`  | Group Separator |
|      | `PT`  | Page Terminator |
| 0x1E | `IS2` | Information Separator Two |
|      | `RS`  | Record Separator |
| 0x1F | `IS1` | Information Separator One |
|      | `US`  | Unit Separator |

### C1 Code Set (ECMA-48)

- Mapped to `CR` Area (0x80-0x9F)
- Also mapped to `ESC` followed by 0x40-0x5F
  - E.g.
    - `ESC` `[` (0x1B 0x5B)  
      ||
    - `CSI` (0x9B)

- Code Table:

| Code | Name  | Description |
|------|-------|-------------|
| 0x80 | -     | -           |
| 0x81 | -     | -           |
| 0x82 | `BPH` | Break Permitted Here |
| 0x83 | `NBH` | No Break Here |
| 0x84 | -     | -           |
| 0x85 | `NEL` | Next Line   |
| 0x86 | `SSA` | Start of Selected Area |
| 0x87 | `ESA` | End of Selected Area |
| 0x88 | `HTS` | Horizontal Tabulation Set |
| 0x89 | `HTJ` | Horizontal Tabulation with Justification |
| 0x8A | `VTS` | Vertical Tabulation Set |
| 0x8B | `PLD` | Partial Line Down |
| 0x8C | `PLU` | Partial Line Up |
| 0x8D | `RI`  | Reverse Index |
| 0x8E | `SS2` | Single Shift Two |
| 0x8F | `SS3` | Single Shift Three |
| 0x90 | `DCS` | Device Control String |
| 0x91 | `PU1` | Private Use One |
| 0x92 | `PU2` | Private Use Two |
| 0x93 | `STS` | Set Transmit State |
| 0x94 | `CCH` | Cancel Character |
| 0x95 | `MW`  | Message Waiting |
| 0x96 | `SPA` | Start of Protected Area |
| 0x97 | `EPA` | End of Protected Area |
| 0x98 | `SOS` | Start of String |
| 0x99 | -     | -           |
| 0x9A | `SCI` | Single Character Introducer |
| 0x9B | `CSI` | Control Sequence Introducer |
| 0x9C | `ST`  | String Terminator |
| 0x9D | `OSC` | Operating System Command |
| 0x9E | `PM`  | Privacy Message |
| 0x9F | `APC` | Application Program Command |

### G0 Code Set (ECMA-6)

- Mapped to `GL` Area (0x20-0x7F) by default

- Code Table:

| Code | Symbol | Code | Symbol | Code | Symbol |
|------|--------|------|--------|------|--------|
| 0x20 | ` `    | 0x40 | `@`    | 0x60 | `` ` `` |
| 0x21 | `!`    | 0x41 | `A`    | 0x61 | `a`    |
| 0x22 | `"`    | 0x42 | `B`    | 0x62 | `b`    |
| 0x23 | `#`    | 0x43 | `C`    | 0x63 | `c`    |
| 0x24 | `$`    | 0x44 | `D`    | 0x64 | `d`    |
| 0x25 | `%`    | 0x45 | `E`    | 0x65 | `e`    |
| 0x26 | `&`    | 0x46 | `F`    | 0x66 | `f`    |
| 0x27 | `'`    | 0x47 | `G`    | 0x67 | `g`    |
| 0x28 | `(`    | 0x48 | `H`    | 0x68 | `h`    |
| 0x29 | `)`    | 0x49 | `I`    | 0x69 | `i`    |
| 0x2A | `*`    | 0x4A | `J`    | 0x6A | `j`    |
| 0x2B | `+`    | 0x4B | `K`    | 0x6B | `k`    |
| 0x2C | `,`    | 0x4C | `L`    | 0x6C | `l`    |
| 0x2D | `-`    | 0x4D | `M`    | 0x6D | `m`    |
| 0x2E | `.`    | 0x4E | `N`    | 0x6E | `n`    |
| 0x2F | `/`    | 0x4F | `O`    | 0x6F | `o`    |
| 0x30 | `0`    | 0x50 | `P`    | 0x70 | `p`    |
| 0x31 | `1`    | 0x51 | `Q`    | 0x71 | `q`    |
| 0x32 | `2`    | 0x52 | `R`    | 0x72 | `r`    |
| 0x33 | `3`    | 0x53 | `S`    | 0x73 | `s`    |
| 0x34 | `4`    | 0x54 | `T`    | 0x74 | `t`    |
| 0x35 | `5`    | 0x55 | `U`    | 0x75 | `u`    |
| 0x36 | `6`    | 0x56 | `V`    | 0x76 | `v`    |
| 0x37 | `7`    | 0x57 | `W`    | 0x77 | `w`    |
| 0x38 | `8`    | 0x58 | `X`    | 0x78 | `x`    |
| 0x39 | `9`    | 0x59 | `Y`    | 0x79 | `y`    |
| 0x3A | `:`    | 0x5A | `Z`    | 0x7A | `z`    |
| 0x3B | `;`    | 0x5B | `[`    | 0x7B | `{`    |
| 0x3C | `<`    | 0x5C | `\`    | 0x7C | `\|`   |
| 0x3D | `=`    | 0x5D | `]`    | 0x7D | `}`    |
| 0x3E | `>`    | 0x5E | `^`    | 0x7E | `~`    |
| 0x3F | `?`    | 0x5F | `_`    |      |        |

| Code | Name  | Description |
|------|-------|-------------|
| 0x7F | `DEL` | Delete      |

## Escape Sequence (ECMA-35)

- An escape sequence consists of:

| Notation    | Description        | Code Range         | Note |
|-------------|--------------------|--------------------|------|
| `ESC`       | Escape             | 0x1B               |      |
| *I* ... *I* | Intermediate Bytes | 0x20-0x2F          | Optional |
| *F*         | Final Byte         | 0x30-0x7E (***1**) |      |

- Note
  - **1*:
    - The function of an escape sequence is specified by the final byte coupled with intermediate bytes.
    - For the final byte, the following codes are reserved for private (or experimental) functions.
      - 0x30-0x3F
        - `0` (0x30)
        - :
        - `9` (0x39)
        - `:` (0x3A)
        - `;` (0x3B)
        - `<` (0x3C)
        - `=` (0x3D)
        - `>` (0x3E)
        - `?` (0x3F)

## Control Sequence (ECMA-48)

- A control sequence consists of:

| Notation    | Description                 | Code Range         | Note |
|-------------|-----------------------------|--------------------|------|
| `CSI`       | Control Sequence Introducer | 0x9B or            |      |
|             |                             | 0x1B 0x5B          | Escape Sequence `ESC` `[` |
| *P* ... *P* | Parameter Bytes             | 0x30-0x3F (***2**) | Optional |
| *I* ... *I* | Intermediate Bytes          | 0x20-0x2F          | Optional |
| *F*         | Final Byte                  | 0x40-0x7E (***1**) |      |

- Note
  - ***1**:
    - The function of a control sequence is specified by the final byte coupled with intermediate bytes.
    - For the final byte, the following codes are reserved for private (or experimental) functions.
      - 0x70-0x7E
        - `p` (0x70)
        - :
        - `z` (0x7A)
        - `{` (0x7B)
        - `|` (0x7C)
        - `}` (0x7D)
        - `~` (0x7E)
  - ***2**:
    - The parameters of a control sequence are specified by the parameter bytes.
    - For the first parameter byte, the following codes are reserved for private (or experimental) parameters.
      - 0x3C-0x3F
        - `<` (0x3C)
        - `=` (0x3D)
        - `>` (0x3E)
        - `?` (0x3F)

## Control String (ECMA-48)

- A control string consists of:

| Element               | Note |
|-----------------------|------|
| Opening Delimiter     | (***1**) |
| String                |      |
| Terminating Delimiter |      |

- The control string for a command string consists of:

| Element               | Notation  |                             | Code Range | Note |
|-----------------------|-----------|-----------------------------|------------|------|
| Opening Delimiter     | `APC`,    | Application Program Command | 0x9F       |      |
|                       | `DCS`,    | Device Control String       | 0x90       | (***2**) |
|                       | `OSC`, or | Operating System Command    | 0x9D       |      |
|                       | `PM`      | Privacy Message             | 0x9E       |      |
| String                | -         | Command String              | (***3**)   |      |
| Terminating Delimiter | `ST`      | String Terminator           | 0x9C       |      |

- The control string for a character string consists of:

| Element               | Notation | Description       | Code Range | Note |
|-----------------------|----------|-------------------|------------|------|
| Opening Delimiter     | `SOS`    | Start of String   | 0x98       |      |
| String                | -        | Character String  | (***4**)   |      |
| Terminating Delimiter | `ST`     | String Terminator | 0x9C       |      |

- Note
  - ***1**:
    - The purpose and format of a control string are specified by the kind of the opening delimiter.
  - ***2**:
    - The purpose and format of a Device Control String (`DCS`) are specified by the most recent Identify Device Control String (`IDCS`) control sequence.
  - ***3**:
    - A command String consists of
      - 0x08-0x0D or 0x20-0x7E
  - ***4**:
    - A character string consists of
      - Any code except `SOS` or `ST`

## References

### Standards

- ecma-international.org
  - [ECMA-6](<https://ecma-international.org/publications-and-standards/standards/ecma-6/>)
    - 7-Bit coded Character Set
    - ISO/IEC number: 646
    - ITU number: T.50
    - [ECMA-6 6th Edition](<https://ecma-international.org/wp-content/uploads/ECMA-6_6th_edition_december_1991.pdf>)
  - [ECMA-35](<https://ecma-international.org/publications-and-standards/standards/ecma-35/>)
    - Character code structure and extension techniques
    - ISO/IEC number: 2022
    - [ECMA-35 6th Edition](<https://ecma-international.org/wp-content/uploads/ECMA-35_6th_edition_december_1994.pdf>)
  - [ECMA-48](<https://ecma-international.org/publications-and-standards/standards/ecma-48/>)
    - Control functions for coded character sets
    - ISO/IEC number: 6429
    - [ECMA-48 Fifth Edition](<https://ecma-international.org/wp-content/uploads/ECMA-48_5th_edition_june_1991.pdf>)

### Explanations

- aivosto.com
  - [Control characters in ASCII and Unicode](<https://www.aivosto.com/articles/control-characters.html>)

### Examples

- compuprint.com
  - [Compuprint 9060-LA Compuprint 9070-LA Programmer’s Manual](<https://www.compuprint.com/docs/archive/9060-70-LA-pm.pdf>)
