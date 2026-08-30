# Tang Primer 20K Dock + 4.3/5.0-inch LCD case R4

Tang Primer 20K Core装着済み公式Dockと、公式4.3インチまたは5.0インチRGB LCDを一体化するFDMケースです。現行バージョンはv1.0.2です。R4は外形を140.00 x 112.00 x 53.80 mmへ拡張し、固定されたリアアクセスフレームと、工具なしで着脱できる20 mmサービスキャップを追加しました。

## 正式成果物

CIまたは`build_release.py`が生成する`release/`だけが現行成果物です。生成物はGitへ直接格納せず、GitHub Actions Artifactを正本とします。旧R3図面・STLは配布物へ含めません。

公式Dock参照STLは`assets/reference/`へxz圧縮・分割して格納し、生成時に連結・展開します。展開後SHA-256は`build_release.py`内で固定・検証します。

| ファイル | 数量 | 用途 |
|---|---:|---|
| `front_shell_43_snap.stl` / `front_shell_50_snap.stl` | どちらか1 | LCD別フロント |
| `lcd_retainer_43_snap.stl` / `lcd_retainer_50_snap.stl` | 対応品1 | LCD押さえ |
| `dock_tray_screw_common.stl` | 1 | Dock四隅ねじ固定 |
| `rear_access_frame_common.stl` | 1 | 外装保持と120 x 92 mmサービス開口 |
| `rear_service_cap_common.stl` | 1 | 着脱式20 mm背面空間、PMOD配線出口 |
| `case_snap_pin.stl` | 4 | 前面から固定フレームまでのねじレス固定 |
| `fit_coupon.stl` | 1 | 造形機別の嵌合確認 |
| `Tang_Primer_20K_Case_R4_Complete_Assembly_43.stl` | 1 | 4.3インチ完成組立・Viewer専用 |
| `Tang_Primer_20K_Case_R4_Complete_Assembly_50.stl` | 1 | 5.0インチ完成組立・Viewer専用 |
| `Tang_Primer_20K_Case_R4_Drawings_1to1.pdf` | 1 | 正式A3図面、13ページ |
| `Tang_Primer_20K_Case_R4_Design_Specification.pdf` | 1 | 設計・組立・サービス仕様 |

完成組立STLと色分け3MFは公式Dock+Core参照メッシュ、LCD、M2.5ねじ、全印刷部品を組立位置に配置しています。重複閉メッシュを含むためスライスせず、格納位置の確認だけに使用してください。FPCは実物ごとに曲げ形状が変わるため含めていません。

## 背面アクセス

- 固定フレームの外面はZ=33.80 mm。従来の37.00 mmケースピンを長くせず、そのまま使用します。
- サービスキャップがZ方向へ20.00 mm追加され、内面はZ=51.40 mm、外面はZ=53.80 mmです。
- 公式Dock+Core STEP最大Z=30.165 mmとの公称余裕は21.235 mmです。
- キャップは上フック2本を先に挿入し、下プッシュタブ2本をクリックさせます。
- 取り外しは下タブ2本を内側へ押し、下辺を起こして上フックを抜きます。ケースピンやDockねじは外しません。
- 下辺に幅20.00 mmの開放切欠きが2か所あり、PMODケーブルを接続したまま着脱できます。

## 固定仕様

- Dock: 公式87.00 x 65.00 mmピッチの四隅穴、M2.5 x 6なべ頭ねじ4本。
- トレイ下穴: 2.00 mm角、深さ4.80 mm、底残り0.80 mm。
- LCD: 外形ポケット、LCDリテーナー、6本のカンチレバー爪。
- Core: DockのSODIMM接点と両側ラッチ。
- FPC: 開放ガイド、コネクタロック、薄手ポリイミドテープ。
- 外装構造: プリント製分割スナップピン4本。
- サービスキャップ: 上フック2本、下プッシュタブ2本。

詳細寸法、組立・分解手順、合格基準は`DESIGN_R4.md`を参照してください。

## 造形

- 材料: PETG推奨
- ノズル: 0.4 mm
- 積層: 0.20 mm以下。サービスキャップのタブは0.16 mm推奨
- 外周: 4周以上。タブは5周推奨
- インフィル: 20～30%、スナップピン100%
- サポート: 不要

STLは納品姿勢のまま造形します。リアアクセスフレームは開口フランジ、サービスキャップは背面格子をベッドへ向けます。係止突起は印刷方向に傾斜成長し、水平な空中開始面を持ちません。

## Nix / Podman開発環境

ローカル生成環境は、`sabas0ba/dotfiles`のcommit `fc4cdecc02a6a95c81a259549d3fb9e7df18bb8f`から構築した`sabas0ba/nixos`を基底とします。プロジェクト固有のPython・PDF依存関係とDejaVuフォントは`flake.nix`と`flake.lock`で固定しています。

```sh
git clone https://github.com/sabas0ba/dotfiles.git
git -C dotfiles checkout fc4cdecc02a6a95c81a259549d3fb9e7df18bb8f
podman build --tag sabas0ba/nixos dotfiles

podman build --file Containerfile --tag sabas0ba/tang-primer-dev .
podman run --rm --volume "$PWD:/workspace" sabas0ba/tang-primer-dev make check
```

Nixが導入済みのホストでは、コンテナを使用せず次の手順でも実行できます。

```sh
nix develop
make check
```

## 再生成と検証

一括生成は次のコマンドで行います。`build/artifact/release/`へ全成果物、`build/artifact/Tang_Primer_20K_LCD_Case_R4.zip`へ配布ZIPを生成し、検証レポートがFAILの場合は終了コード1で停止します。

```sh
python3 -m pip install --requirement requirements-drawings.txt
python3 -m unittest discover -s tests -v
python3 build_release.py
```

GitHub Actionsの`Build release artifact`はpush、pull request、手動実行で同じ手順を実行します。成功時は`Tang_Primer_20K_LCD_Case_R4.zip`と展開済み`release/`一式を、commit SHA付きArtifactとして30日間保存します。

`v1.2.3`または`v1.2.3-rc.1`形式のtagをpushすると、`Publish release`が同じテスト・生成・検証を実行し、対応するGitHub Releaseへ配布ZIPとZIP用SHA-256ファイルを添付します。既存Releaseに対する再実行では同名assetを置換します。ハイフンを含むtagはprereleaseとして作成します。

個別確認する場合は、まず一括生成した`build/artifact/release/`を入力に使用します。

```sh
python3 build_release.py
python3 generate_release_drawings.py --input build/artifact/release --dock-step-stl build/artifact/release/reference/dock3713_assembly.stl --output build/artifact/release/Tang_Primer_20K_Case_R4_Drawings_1to1.pdf
python3 generate_reference_3mf_r4.py --input build/artifact/release --dock-step-stl build/artifact/release/reference/dock3713_assembly.stl --spec 43 --output build/artifact/release/Tang_Primer_20K_Case_R4_Reference_Assembly_43.3mf
python3 generate_assembled_stl_r4.py --input build/artifact/release --dock-step-stl build/artifact/release/reference/dock3713_assembly.stl --spec 43 --output build/artifact/release/Tang_Primer_20K_Case_R4_Complete_Assembly_43.stl
python3 -m unittest discover -s tests -v
```

図面は納品STLから直接三面図を投影し、組立断面は納品STLと公式Dock参照メッシュを交差させて生成します。1:1図面はA3用紙へ100%で印刷し、用紙合わせを無効にしてください。

初回は`fit_coupon.stl`、ケースピン1本、`rear_service_cap_common.stl`を先に造形し、穴補正、タブの係止力と指での解除を確認してください。落下、車載、長期振動、防水、安全規格は未評価です。
